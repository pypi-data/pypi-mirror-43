import os
from collections import Counter
from imageatm.handlers.images import resize_image_mp, validate_image
from imageatm.handlers.utils import load_json, save_json, parallelise
from imageatm.handlers.logger import get_logger
from sklearn.model_selection import train_test_split


class DataPrep:
    '''Prepares data for training.

    Attributes:
        image_dir: path of image directory
        job_dir: path to job directory with samples
    '''

    def __init__(
        self,
        job_dir,
        image_dir,
        samples_file,
        min_class_size=2,
        test_size=0.2,
        val_size=0.1,
        part_size=1,
    ):
        '''
        Inits data preparation object.

        Load samples file.
        Initialize variables for further operations:
        valid_image_ids, class_mapping, train_samples, val_samples, test_samples
        '''
        self.job_dir = job_dir

        self.logger = get_logger(__name__, self.job_dir)
        self.image_dir = image_dir
        self.samples_file = samples_file
        self.min_class_size = min_class_size
        self.test_size = test_size
        self.val_size = val_size
        self.part_size = part_size

        self.valid_image_ids = None
        self.class_mapping = None
        self.train_samples = None
        self.val_samples = None
        self.test_samples = None

        self.samples = load_json(self.samples_file)

    def prepare_data(self, resize=False):
        '''Executes all steps of data preparation.'''
        self.validate_images()
        self.validate_samples()
        self.get_class_mapping()
        self.convert_label_to_int()
        self.split_samples()

        if resize:
            self.resize_images()

        self.save_files()

    def get_counter(self, list_to_count, print_count=False):
        counter = Counter(list_to_count)
        total = len(list_to_count)

        if print_count:
            for key, val in sorted(counter.items()):
                self.logger.info('{}: {} ({}%)'.format(key, val, round(val * 100 / total, 1)))

        return counter

    def get_samples_count(self, print_count=True):
        '''Retrieves samples count for each label from loaded samples.'''
        self.samples_count = self.get_counter([i['label'] for i in self.samples], print_count)

    def validate_images(self):
        '''Checks if all files in image_dir are valid images.

        Checks if files are images with extention 'JPEG' or 'PNG' and if they are not truncated.
        self.logger.infos filenames that didn't pass the validationself.

        Sets:
            self.valid_image_ids: a list of valid image
        '''
        self.logger.info('\n****** Running image validation ******\n')

        # validate images, use multiprocessing
        files = [os.path.join(self.image_dir, i) for i in os.listdir(self.image_dir)]
        results = parallelise(validate_image, files)

        valid_image_files = [j for i, j in enumerate(files) if results[i][0]]
        self.valid_image_ids = [os.path.basename(i) for i in valid_image_files]

        # return list of invalid images to user and save them if there are more than 10
        invalid_image_files = [(j, results[i][1]) for i, j in enumerate(files) if not results[i][0]]

        if invalid_image_files:
            self.logger.info('The following files are not valid image files:')
            for file_name, error_msg in invalid_image_files[:10]:
                self.logger.info('- {} ({})'.format(file_name, error_msg))
            if len(invalid_image_files) > 10:
                save_json(
                    invalid_image_files, os.path.join(self.job_dir, 'invalid_image_files.json')
                )
                self.logger.info(
                    (
                        'NOTE: More than 10 files were identified as invalid image files.\n'
                        'The full list of those files has been saved here:\n{}'.format()
                    )
                )

    @staticmethod
    def _validate_sample(sample, valid_image_ids):
        return all(
            [
                ('label' in sample),
                ('image_id' in sample),
                (sample.get('image_id') in valid_image_ids),
            ]
        )

    def validate_samples(self):
        '''Validates the samples.

        Compares samples with valid image ids.
        Checks if :
            - samples have 'label' and 'image_id' keys
            - there is more than 1 class
            - there are enough samples in each class

        Reassigns self.samples to valid samples.
        self.logger.infos:
            - samples that didn't pass the validationself
            - distribution of valid samples for each label
        '''
        # images have to be validated before samples can be validated
        if not self.valid_image_ids:
            self.validate_images()

        self.logger.info('\n****** Running samples validation ******\n')

        valid_image_ids = set(self.valid_image_ids)  # convert to set to optimise lookup

        # exclude samples with invalid image or invalid keys
        valid_samples = []
        self.invalid_samples = []
        for sample in self.samples:
            if self._validate_sample(sample, valid_image_ids):
                valid_samples.append(sample)
            else:
                self.invalid_samples.append(sample)

        # replace self.samples with valid samples
        assert valid_samples, 'Program ended. No valid samples found.'
        self.samples = valid_samples

        # self.logger.infos invalid images to user and saves them in json if there are more than 10
        if self.invalid_samples:
            self.logger.info('The following samples were dropped:')
            for sample in self.invalid_samples[:10]:
                self.logger.info('- {}'.format(sample))

            if len(self.invalid_samples) > 10:
                self.logger.info(
                    (
                        'NOTE: {} samples were identified as invalid.\n'
                        'The full list of invalid samples will be saved in job dir.\n'.format(
                            len(self.invalid_samples)
                        )
                    )
                )

        self.logger.info('Class distribution after validation:')
        self.get_samples_count()

        # check if each class has sufficient samples
        warnings_count = 0
        for key, val in self.samples_count.items():
            if val < self.min_class_size:
                warnings_count += 1
                self.logger.info('Not enough samples for label {}'.format(key))

        assert warnings_count == 0, 'Program ended. Collect more samples.'
        assert len(self.samples_count) > 1, 'Program ended. Only one label in the dataset.'

    def get_class_mapping(self, print_mapping=True):
        self.get_samples_count(print_count=False)

        self.class_mapping = {}
        labels = list(self.samples_count.keys())
        labels.sort()

        for i, j in enumerate(labels):
            self.class_mapping[i] = j

        if print_mapping:
            self.logger.info('Class mapping:\n{}'.format(self.class_mapping))

    def convert_label_to_int(self):
        self.get_class_mapping(print_mapping=False)

        class_mapping_inv = {v: k for k, v in self.class_mapping.items()}

        samples_int = [
            {'label': class_mapping_inv[sample['label']], 'image_id': sample['image_id']}
            for sample in self.samples
        ]

        # replace self.samples with samples int
        self.samples = samples_int

    def split_samples(self):
        '''Produces stratified train, val, test sets.

        The test proportion is applied first, then val proportion,
        i.e. if test_size=0.2 and val_size=0.1,
        then train_size=0.72 ((1-0.2)*0.9).

        Sets:
            self.train_samples, self.val_samples, self.test_samples
        '''
        self.logger.info('\n****** Creating train/val/test sets ******\n')

        self.train_size = 1 - (self.test_size + self.val_size)

        self.logger.info(
            'Split distribution: train: {:.2f}, val: {}, test: {:}\n'.format(
                self.train_size, self.val_size, self.test_size
            )
        )

        self.logger.info(
            'Partial split distribution: train: {:.2f}, val: {:.2f}, test: {:.2f}\n'.format(
                self.train_size * self.part_size,
                self.val_size * self.part_size,
                self.test_size * self.part_size,
            )
        )

        labels = [i['label'] for i in self.samples]  # need label list for stratification

        split_test_size = self.test_size * self.part_size
        split_train_size = (1 - self.test_size) * self.part_size

        train_samples, self.test_samples, train_labels, _ = train_test_split(
            self.samples,
            labels,
            test_size=split_test_size,
            train_size=split_train_size,
            shuffle=True,
            random_state=10207,
            stratify=labels,
        )

        split_test_size = self.val_size / (1 - self.test_size)
        self.train_samples, self.val_samples, _, _ = train_test_split(
            train_samples,
            train_labels,
            test_size=split_test_size,
            shuffle=True,
            random_state=10207,
            stratify=train_labels,
        )

        self.logger.info('Train set:')
        self.get_counter([i['label'] for i in self.train_samples], print_count=True)

        self.logger.info('Val set:')
        self.get_counter([i['label'] for i in self.val_samples], print_count=True)

        self.logger.info('Test set:')
        self.get_counter([i['label'] for i in self.test_samples], print_count=True)

    def resize_images(self, resize_image_mp=resize_image_mp):
        self.logger.info('\n****** Resizing images ******\n')
        new_image_dir = os.path.join(self.image_dir, '_resized')
        if not os.path.exists(new_image_dir):
            os.makedirs(new_image_dir)

        args = [(self.image_dir, new_image_dir, i['image_id']) for i in self.samples]
        parallelise(resize_image_mp, args)
        self.logger.info(
            'Stored {} resized images under {}'.format(len(self.samples), new_image_dir)
        )

        self.image_dir = new_image_dir
        self.logger.info('Changed image directory to {}'.format(self.image_dir))

    def save_files(self, dir=None):
        if dir:
            self.job_dir = dir
            if not os.path.exists(dir):
                os.makedirs(dir)

        else:
            self.job_dir = os.path.abspath(self.job_dir)

        if not self.train_samples:
            self.split_samples()

        if not self.class_mapping:
            self.get_class_mapping()

        save_json(self.train_samples, os.path.join(self.job_dir, 'train_samples.json'))
        save_json(self.val_samples, os.path.join(self.job_dir, 'val_samples.json'))
        save_json(self.test_samples, os.path.join(self.job_dir, 'test_samples.json'))
        save_json(self.class_mapping, os.path.join(self.job_dir, 'class_mapping.json'))

        if len(self.invalid_samples) > 10:
            save_json(self.invalid_samples, os.path.join(self.job_dir, 'invalid_samples.json'))
            self.logger.info(
                (
                    'NOTE: More than 10 samples were identified as invalid.\n'
                    'The full list of invalid samples has been saved here:\n{}'.format(
                        os.path.join(self.job_dir, 'invalid_samples.json')
                    )
                )
            )
