from imageatm.handlers.image_classifier import ImageClassifier
from keras.models import Model
from keras.layers import Dropout, Dense

TEST_CONFIG =  {
    "base_model_name": "MobileNet",
    "batch_size": 16,
    "decay_all": 0,
    "decay_dense": 0,
    "dropout_rate": 0.75,
    "epochs_train_all": 5,
    "epochs_train_dense": 5,
    "learning_rate_all": 0.0000003,
    "learning_rate_dense": 0.001,
    "multiprocessing_data_load": True,
    "num_workers_data_load": 8,
    "n_classes": 10,
    "loss": "categorical_crossentropy"
}

def test__init():
    classifier = ImageClassifier(TEST_CONFIG['base_model_name'],
                                 TEST_CONFIG['n_classes'],
                                 TEST_CONFIG['learning_rate_dense'],
                                 TEST_CONFIG['dropout_rate'],
                                 TEST_CONFIG['loss']
                                 )

    assert classifier.weights == 'imagenet'

# def test__build(mocker):
#     mocker.patch('keras.layers.Dropout.__init__')
#     Dropout.__init__.return_value = None
#     mocker.patch('keras.layers.Dense.__init__')
#     Dense.__init__.return_value = None
#
#     classifier = ImageClassifier(TEST_CONFIG['base_model_name'],
#                                  TEST_CONFIG['n_classes'],
#                                  TEST_CONFIG['learning_rate_dense'],
#                                  TEST_CONFIG['dropout_rate'],
#                                  decay=TEST_CONFIG['decay_dense'])
#     classifier.build()
#     pass

# def test__fit_generator(mocker):
#     mocker.patch('keras.models.Model.fit_generator')
#     mocker.patch('keras.layers.Dropout.__init__')
#     mocker.patch('keras.layers.Dense.__init__')
#
#     classifier = ImageClassifier(TEST_CONFIG['base_model_name'],
#                                  TEST_CONFIG['n_classes'],
#                                  TEST_CONFIG['learning_rate_dense'],
#                                  TEST_CONFIG['dropout_rate'],
#                                  decay=TEST_CONFIG['decay_dense'])
#
#     classifier.fit_generator(generator='training_generator',
#                              validation_data='validation_generator',
#                              epochs=TEST_CONFIG['epochs_train_dense'],
#                              verbose=1,
#                              use_multiprocessing=TEST_CONFIG['multiprocessing_data_load'],
#                              workers=TEST_CONFIG['num_workers_data_load'],
#                              max_queue_size=30,
#                              callbacks=[])
#
#     # Model.fit_generator.assert_called()
#     # classifier.accept_parameter.assert_called()
#
#     pass