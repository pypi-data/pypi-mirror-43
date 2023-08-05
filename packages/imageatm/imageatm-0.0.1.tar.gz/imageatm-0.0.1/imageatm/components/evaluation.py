import os
import glob
import itertools
import numpy as np
import matplotlib.pyplot as plt
from imageatm.handlers.images import load_image
from imageatm.handlers.image_classifier import ImageClassifier
from imageatm.handlers.data_generator import ValDataGenerator
from imageatm.handlers.utils import load_json
from imageatm.handlers.keras_utils import use_multiprocessing, load_model
from imageatm.handlers.logger import get_logger
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from vis.visualization import visualize_cam


BATCH_SIZE = 16
BASE_MODEL_NAME = 'MobileNet'

USE_MULTIPROCESSING, WORKERS = use_multiprocessing()


class Evaluation:
    """Evaluates saved model.

    Attributes:
        image_dir: path of image directory
        job_dir: path to job directory with samples
    """

    def __init__(self, image_dir, job_dir, batch_size=BATCH_SIZE, base_model_name=BASE_MODEL_NAME):
        """Inits Evaluation class with image_dir, job_dir, batch_size, base_model_name.

        Load test set and class mapping.
        Define variables: classes, n_classes, y_true, y_pred.
        Load the model with best available accuracy.
        """
        self.image_dir = os.path.abspath(image_dir)
        self.job_dir = os.path.abspath(job_dir)

        self.logger = get_logger(__name__, self.job_dir)
        self.samples_test = load_json(os.path.join(self.job_dir, 'test_samples.json'))
        self.class_mapping = load_json(os.path.join(self.job_dir, 'class_mapping.json'))
        self.n_classes = len(self.class_mapping.keys())
        self.classes = [str(self.class_mapping[str(i)]) for i in range(self.n_classes)]
        self.y_true = np.array([i['label'] for i in self.samples_test])
        self.batch_size = batch_size
        self.base_model_name = base_model_name

        self._set_plots()
        self._set_best_model()
        self._set_evaluation_dir()

    def _set_plots(self):
        ''' Checks whether ipython kernel is present.

        Plots will only be shown if in ipython, otherwise saved as files.
        '''
        try:
            __IPYTHON__
            self.show_plots = True
            self.save_plots = False
        except NameError:
            self.show_plots = False
            self.save_plots = True

    def _set_best_model(self):
        self.logger.info('\n****** Loading model ******\n')
        self.best_model, self.best_model_file = self._load_best_model()

    def _set_evaluation_dir(self):
        if self.save_plots:
            evaluation_dir_name = os.path.basename(self.best_model_file).split('.hdf5')[0]
            self.evaluation_dir = os.path.join(
                self.job_dir, 'evaluation_{}'.format(evaluation_dir_name)
            )
            if not os.path.exists(self.evaluation_dir):
                os.makedirs(self.evaluation_dir)

    def _load_best_model(self):
        model_files = glob.glob(os.path.join(self.job_dir, 'models', '*.hdf5'))
        max_acc_idx = np.argmax([os.path.basename(m).split('_')[3][:5] for m in model_files])
        best_model_file = model_files[max_acc_idx]
        best_model = load_model(best_model_file)
        self.logger.info('loaded {}\n'.format(best_model_file))
        return best_model, best_model_file

    def run(self):
        self.logger.info('\n****** Test set distribution ******\n')
        self.plot_test_set_distribution()

        self.classifier = ImageClassifier(
            base_model_name=self.base_model_name,
            n_classes=self.n_classes,
            weights=None,
            dropout_rate=None,
            learning_rate=None,
            loss=None,
        )
        self.classifier.model = self.best_model

        self.data_generator = ValDataGenerator(
            samples=self.samples_test,
            img_dir=self.image_dir,
            batch_size=self.batch_size,
            n_classes=self.n_classes,
            basenet_preprocess=self.classifier.get_preprocess_input(),
        )

        self.logger.info('\n****** Get predictions from test set ******\n')
        predictions_dist = self.classifier.predict_generator(
            data_generator=self.data_generator,
            workers=WORKERS,
            use_multiprocessing=USE_MULTIPROCESSING,
            verbose=1,
        )

        self.y_pred = np.argmax(predictions_dist, axis=1)
        self.accuracy = accuracy_score(y_true=self.y_true, y_pred=self.y_pred)

        self.logger.info(
            '\nModel achieves {}% accuracy on test set\n'.format(round(self.accuracy * 100, 2))
        )

        self.logger.info(self.classification_report())
        self.plot_confusion_matrix()

    def classification_report(self):
        return classification_report(
            y_true=self.y_true, y_pred=self.y_pred, target_names=self.classes
        )

    def confusion_matrix(self):
        return confusion_matrix(y_true=self.y_true, y_pred=self.y_pred)

    def plot_test_set_distribution(self):
        """Plots bars with number of samples for each label in test set."""
        counts = np.bincount(self.y_true)
        title = 'Number of images in test set: {}'.format(len(self.samples_test))
        index = np.arange(self.n_classes)
        title_fontsize = 16 if self.n_classes < 4 else 18
        text_fontsize = 12 if self.n_classes < 4 else 14

        plt.bar(index, counts)
        plt.xlabel('Label', fontsize=text_fontsize)
        plt.ylabel('Number of images', fontsize=text_fontsize)
        plt.xticks(index, self.classes, fontsize=text_fontsize, rotation=30)
        plt.title(title, fontsize=title_fontsize)

        # figsize = [min(15, self.n_classes * 2), 5]
        # plt.figure(figsize=figsize)
        plt.tight_layout()

        if self.save_plots:
            target_file = os.path.join(self.evaluation_dir, 'test_set_distribution.pdf')
            plt.savefig(target_file)
            self.logger.info('saved under {}'.format(target_file))

        if self.show_plots:
            plt.show()

    def plot_confusion_matrix(self):
        """Plots normalized confusion matrix."""
        cm = self.confusion_matrix()
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        figsize = [min(15, self.n_classes * 3.5), min(15, self.n_classes * 3.5)]
        title_fontsize = 16 if self.n_classes < 4 else 18
        text_fontsize = 12 if self.n_classes < 4 else 14
        self.logger.info(figsize)
        plt.figure(figsize=figsize)
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion matrix', fontsize=title_fontsize)
        plt.colorbar()
        tick_marks = np.arange(self.n_classes)
        plt.xticks(tick_marks, self.classes, rotation=45, fontsize=text_fontsize)
        plt.yticks(tick_marks, self.classes, fontsize=text_fontsize)
        plt.ylabel('True label', fontsize=text_fontsize)
        plt.xlabel('Predicted label', fontsize=text_fontsize)

        thresh = cm.max() / 2.0
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(
                j,
                i,
                '{:.2f}'.format(cm[i, j]),
                horizontalalignment='center',
                color='white' if cm[i, j] > thresh else 'black',
                fontsize=text_fontsize,
            )

        plt.tight_layout()

        if self.save_plots:
            target_file = os.path.join(self.evaluation_dir, 'confusion_matrix.pdf')
            plt.savefig(target_file)
            self.logger.info('saved under {}'.format(target_file))

        if self.show_plots:
            plt.show()

    # get all misclassified images:
    def get_correct_wrong_examples(self, label):
        """Gets correctly and wrongly predicted samples for a given label.

        Attributes:
            label: int or str (label for which the predictions should be considered)
        """
        correct = []
        wrong = []

        if type(label) == str:
            class_mapping_inv = {v: k for k, v in self.class_mapping.items()}
            label = int(class_mapping_inv[label])

        for i, sample in enumerate(self.samples_test):
            if self.y_true[i] == label:
                image_file = os.path.join(self.image_dir, sample['image_id'])
                if self.y_true[i] == self.y_pred[i]:
                    correct.append([i, load_image(image_file, target_size=(224, 224)), sample])
                else:
                    wrong.append([i, load_image(image_file, target_size=(224, 224)), sample])

        return correct, wrong

    # visualize misclassified images:
    def visualize_images(self, image_list, show_heatmap=False, n_plot=20):
        """Visualizes images in a sample list.

        Attributes:
            imgae_list: sample list
            show_heatmap: boolean (generates a gradient based class activation map (grad-CAM))
        """
        n_rows = min(n_plot, len(image_list))
        n_cols = 2 if show_heatmap else 1

        figsize = [5 * n_cols, 5 * n_rows]
        plt.figure(figsize=figsize)

        plot_count = 1
        for (i, img, sample) in image_list[:n_rows]:
            plt.subplot(n_rows, n_cols, plot_count)
            plt.imshow(img)
            plt.axis('off')
            plt.title(
                'true: {}, predicted: {}'.format(
                    self.class_mapping[str(self.y_true[i])], self.class_mapping[str(self.y_pred[i])]
                )
            )
            plot_count += 1

            if show_heatmap is True:
                heatmap = visualize_cam(
                    model=self.classifier.model,
                    layer_idx=89,
                    filter_indices=[self.y_pred[i]],
                    seed_input=self.classifier.get_preprocess_input()(
                        np.array(img).astype(np.float32)
                    ),
                )
                plt.subplot(n_rows, n_cols, plot_count)
                plt.imshow(img)
                plt.imshow(heatmap, alpha=0.7)
                plt.axis('off')
                plot_count += 1

        if self.save_plots:
            # TODO: pass name as argument
            target_file = os.path.join(self.evaluation_dir, 'misclassified_images.pdf')
            plt.savefig(target_file)
            self.logger.info('saved under {}'.format(target_file))

        if self.show_plots:
            plt.show()
