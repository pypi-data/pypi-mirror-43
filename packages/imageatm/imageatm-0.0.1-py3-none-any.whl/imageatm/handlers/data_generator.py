import os
import numpy as np
from imageatm.handlers.images import load_image, random_crop
from keras.utils import Sequence, to_categorical


class DataGenerator(Sequence):
    '''inherits from Keras Sequence base object, allows to use multiprocessing in .fit_generator'''

    def __init__(
        self, samples, img_dir, batch_size, n_classes, basenet_preprocess, img_load_dims, train
    ):
        self.samples = samples
        self.img_dir = img_dir
        self.batch_size = batch_size
        self.n_classes = n_classes
        self.basenet_preprocess = basenet_preprocess  # basenet specific preprocessing function
        self.img_load_dims = img_load_dims  # dimensions that images get resized into when loaded
        self.train = train
        self.on_epoch_end()  # call ensures that samples are shuffled in first epoch if shuffle is set to True

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.samples))
        if self.train is True:
            np.random.shuffle(self.indexes)

    def __len__(self):
        return int(np.ceil(len(self.samples) / self.batch_size))  # number of batches per epoch

    def __getitem__(self, index):
        batch_indexes = self.indexes[
            index * self.batch_size : (index + 1) * self.batch_size
        ]  # get batch indexes
        batch_samples = [self.samples[i] for i in batch_indexes]  # get batch samples
        X, y = self.data_generator(batch_samples)
        return X, y

    def data_generator(self, batch_samples):
        # initialize images and labels tensors for faster processing
        dims = self.img_crop_dims if self.train == True else self.img_load_dims
        X = np.empty((len(batch_samples), *dims, 3))
        y = np.empty((len(batch_samples), self.n_classes))

        for i, sample in enumerate(batch_samples):
            # load and randomly augment image
            img_file = os.path.join(self.img_dir, sample['image_id'])
            img = np.asarray(load_image(img_file, self.img_load_dims))
            if self.train == True:
                img = random_crop(img, self.img_crop_dims)
            X[i,] = img

            # TODO: more efficient by preprocessing
            y[i,] = to_categorical([sample['label']], num_classes=self.n_classes)

        # apply basenet specific preprocessing
        # input is 4D numpy array of RGB values within [0, 255]
        X = self.basenet_preprocess(X)

        return X, y


class TrainDataGenerator(DataGenerator):
    def __init__(
        self,
        samples,
        img_dir,
        batch_size,
        n_classes,
        basenet_preprocess,
        img_load_dims=(256, 256),
        img_crop_dims=(224, 224),
        train=True,
    ):
        super(TrainDataGenerator, self).__init__(
            samples, img_dir, batch_size, n_classes, basenet_preprocess, img_load_dims, train
        )
        self.img_crop_dims = img_crop_dims  # dimensions that images get randomly cropped to


class ValDataGenerator(DataGenerator):
    def __init__(
        self,
        samples,
        img_dir,
        batch_size,
        n_classes,
        basenet_preprocess,
        img_load_dims=(224, 224),
        train=False,
    ):
        super(ValDataGenerator, self).__init__(
            samples, img_dir, batch_size, n_classes, basenet_preprocess, img_load_dims, train
        )
