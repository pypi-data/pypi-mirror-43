import importlib
from keras.models import Model
from keras.layers import Dropout, Dense
from keras.optimizers import Adam


class ImageClassifier:
    def __init__(
        self, base_model_name, n_classes, learning_rate, dropout_rate, loss, weights='imagenet'
    ):
        self.n_classes = n_classes
        self.base_model_name = base_model_name
        self.learning_rate = learning_rate
        self.dropout_rate = dropout_rate
        self.loss = loss
        self.weights = weights
        self.__load_base_module()

    def __load_base_module(self):
        # import Keras base model module
        if self.base_model_name == 'InceptionV3':
            self.base_module = importlib.import_module('keras.applications.inception_v3')
        elif self.base_model_name == 'InceptionResNetV2':
            self.base_module = importlib.import_module('keras.applications.inception_resnet_v2')
        else:
            self.base_module = importlib.import_module(
                'keras.applications.' + self.base_model_name.lower()
            )

    def get_base_layers(self):
        return self.base_model.layers

    def get_preprocess_input(self):
        return self.base_module.preprocess_input

    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate

    def build(self):
        # get base model class
        BaseCnn = getattr(self.base_module, self.base_model_name)

        # load pre-trained model
        self.base_model = BaseCnn(
            input_shape=(224, 224, 3), weights=self.weights, include_top=False, pooling='avg'
        )

        # add dropout and dense layer
        x = Dropout(self.dropout_rate)(self.base_model.output)
        x = Dense(units=self.n_classes, activation='softmax')(x)

        self.model = Model(self.base_model.inputs, x)

    def compile(self):
        self.model.compile(
            optimizer=Adam(lr=self.learning_rate), loss=self.loss, metrics=['accuracy']
        )

    def fit_generator(self, **kwargs):
        self.model.fit_generator(**kwargs)

    def predict_generator(self, data_generator, **kwargs):
        return self.model.predict_generator(data_generator, **kwargs)

    def summary(self):
        self.model.summary()
