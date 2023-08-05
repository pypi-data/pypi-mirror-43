import os
import numpy as np
import tensorflow as tf
from imageatm.handlers.data_generator import TrainDataGenerator, ValDataGenerator
from imageatm.handlers.image_classifier import ImageClassifier
from imageatm.handlers.utils import load_json
from imageatm.handlers.keras_utils import use_multiprocessing, LoggingMetrics, LoggingModels
from imageatm.handlers.logger import get_logger
from keras import backend as K
from keras.callbacks import ReduceLROnPlateau, EarlyStopping

tf.logging.set_verbosity(tf.logging.ERROR)

LEARNING_RATE_DENSE = 0.001
LEARNING_RATE_ALL = 0.0001
BATCH_SIZE = 64
DROPOUT_RATE = 0.75
BASE_MODEL_NAME = 'MobileNet'
LOSS = 'categorical_crossentropy'


class Training:
    def __init__(
        self,
        image_dir,
        job_dir,
        epochs_train_dense=None,  # if None then will be set based on number of samples
        epochs_train_all=None,  # if None then will be set based on number of samples
        learning_rate_dense=LEARNING_RATE_DENSE,
        learning_rate_all=LEARNING_RATE_ALL,
        batch_size=BATCH_SIZE,
        dropout_rate=DROPOUT_RATE,
        base_model_name=BASE_MODEL_NAME,
        loss=LOSS,
        **kwargs
    ):

        self.image_dir = os.path.abspath(image_dir)
        self.job_dir = os.path.abspath(job_dir)

        self.logger = get_logger(__name__, self.job_dir)
        self.samples_train = load_json(os.path.join(self.job_dir, 'train_samples.json'))
        self.samples_val = load_json(os.path.join(self.job_dir, 'val_samples.json'))
        self.class_mapping = load_json(os.path.join(self.job_dir, 'class_mapping.json'))
        self.n_classes = len(self.class_mapping.keys())

        self.epochs_train_dense = epochs_train_dense
        self.epochs_train_all = epochs_train_all
        self.learning_rate_dense = float(learning_rate_dense)
        self.learning_rate_all = float(learning_rate_all)
        self.batch_size = int(batch_size)
        self.dropout_rate = float(dropout_rate)
        self.base_model_name = base_model_name
        self.loss = loss
        self.use_multiprocessing, self.workers = use_multiprocessing()
        self.calc_epochs_train()

    def build_model(self):
        self.classifier = ImageClassifier(
            self.base_model_name,
            self.n_classes,
            self.learning_rate_dense,
            self.dropout_rate,
            self.loss,
        )
        self.classifier.build()

    def fit_model(self):
        training_generator = TrainDataGenerator(
            self.samples_train,
            self.image_dir,
            self.batch_size,
            self.n_classes,
            self.classifier.get_preprocess_input(),
        )

        validation_generator = ValDataGenerator(
            self.samples_val,
            self.image_dir,
            self.batch_size,
            self.n_classes,
            self.classifier.get_preprocess_input(),
        )

        # TODO: initialize callbacks TensorBoardBatch and ModelCheckpoint
        # tensorboard = TensorBoardBatch(log_dir=os.path.join(job_dir, 'logs'))

        model_save_name = (
            'model_' + self.base_model_name.lower() + '_{epoch:02d}_{val_acc:.3f}.hdf5'
        )
        model_dir = os.path.join(self.job_dir, 'models')
        if not os.path.isdir(model_dir):
            os.makedirs(model_dir)

        logging_metrics = LoggingMetrics(logger=self.logger)
        logging_models = LoggingModels(
            logger=self.logger,
            filepath=os.path.join(model_dir, model_save_name),
            monitor='val_acc',
            verbose=1,
            save_best_only=True,
            save_weights_only=False,
        )

        def __train_dense_layers():
            if self.epochs_train_dense > 0:
                self.logger.info('\n****** Train dense layers ******\n')

                # freeze convolutional layers in base net
                for layer in self.classifier.get_base_layers():
                    layer.trainable = False

                self.classifier.compile()
                # self.classifier.summary()

                self.hist_dense = self.classifier.fit_generator(
                    generator=training_generator,
                    validation_data=validation_generator,
                    epochs=self.epochs_train_dense,
                    verbose=1,
                    use_multiprocessing=self.use_multiprocessing,
                    workers=self.workers,
                    max_queue_size=30,
                    callbacks=[logging_metrics, logging_models],
                )

        def __train_all_layers():
            if self.epochs_train_all > 0:
                self.logger.info('\n****** Train all layers ******\n')

                min_lr = self.learning_rate_all / 10
                reduce_lr = ReduceLROnPlateau(
                    monitor='val_acc', factor=0.3162, patience=5, min_lr=min_lr, verbose=1
                )

                early_stopping = EarlyStopping(
                    monitor='val_acc',
                    min_delta=0,
                    patience=15,
                    verbose=1,
                    mode='auto',
                    baseline=None,
                    restore_best_weights=False,
                )

                # unfreeze all layers
                for layer in self.classifier.get_base_layers():
                    layer.trainable = True

                self.classifier.set_learning_rate(self.learning_rate_all)

                self.classifier.compile()
                # self.classifier.summary()

                self.hist_all = self.classifier.fit_generator(
                    generator=training_generator,
                    validation_data=validation_generator,
                    epochs=self.epochs_train_dense + self.epochs_train_all,
                    initial_epoch=self.epochs_train_dense,
                    verbose=1,
                    use_multiprocessing=self.use_multiprocessing,
                    workers=self.workers,
                    max_queue_size=30,
                    callbacks=[logging_metrics, logging_models, reduce_lr, early_stopping],
                )

        __train_dense_layers()
        __train_all_layers()

        K.clear_session()

    def calc_epochs_train(self):
        '''
        we assume a simplified logic behind the interpolation: 100/2^(log(x)-1)
        '''
        x = len(self.samples_train)

        if self.epochs_train_dense is None:
            self.epochs_train_dense = int(100 / (2 ** (np.log10(x) - 1)))
        else:
            self.epochs_train_dense = int(self.epochs_train_dense)

        if self.epochs_train_all is None:
            self.epochs_train_all = int(100 / (2 ** (np.log10(x) - 1)))
        else:
            self.epochs_train_all = int(self.epochs_train_all)

    def train(self):
        self.build_model()
        self.fit_model()
