from imageatm.components.training import Training
from imageatm.handlers.image_classifier import ImageClassifier

## TODO: relative path instead of hard-coded
TEST_IMAGE_DIR = './tests/test_images'
TEST_JOB_DIR = './tests/test_train_job'


def test__init():
    train = Training(image_dir=TEST_IMAGE_DIR, job_dir=TEST_JOB_DIR)
    assert train.n_classes == 2
    assert train.epochs_train_dense == 131


def test__build_model(mocker):
    mocker.patch('imageatm.handlers.image_classifier.ImageClassifier.__init__')
    ImageClassifier.__init__.return_value = None
    mocker.patch('imageatm.handlers.image_classifier.ImageClassifier.build')

    ## TODO: init is duplicate here
    train = Training(image_dir=TEST_IMAGE_DIR, job_dir=TEST_JOB_DIR)
    train.build_model()

    ImageClassifier.__init__.assert_called_once_with('MobileNet', 2, 0.001, 0.75, 'categorical_crossentropy')
    ImageClassifier.build.assert_called_once_with()


def test__fit_model(mocker):
    ## TODO: mocker-code is duplicate
    mocker.patch('imageatm.handlers.image_classifier.ImageClassifier.__init__')
    ImageClassifier.__init__.return_value = None
    mocker.patch('imageatm.handlers.image_classifier.ImageClassifier.build')
    mocker.patch('imageatm.handlers.image_classifier.ImageClassifier.compile')
    mocker.patch('imageatm.handlers.image_classifier.ImageClassifier.fit_generator')
    mocker.patch('imageatm.handlers.image_classifier.ImageClassifier.summary')
    mocker.patch('imageatm.handlers.image_classifier.ImageClassifier.get_preprocess_input')
    mocker.patch('imageatm.handlers.image_classifier.ImageClassifier.get_base_layers')

    ## TODO: init and build is duplicate here
    train = Training(image_dir=TEST_IMAGE_DIR, job_dir=TEST_JOB_DIR)
    train.build_model()
    train.fit_model()

    # TODO: this tests are only rudimentary
    ImageClassifier.compile.assert_called_with()
    # ImageClassifier.summary.assert_called_with()
    ImageClassifier.fit_generator.assert_called()
    ImageClassifier.get_base_layers.assert_called()
    ImageClassifier.get_preprocess_input.assert_called()
