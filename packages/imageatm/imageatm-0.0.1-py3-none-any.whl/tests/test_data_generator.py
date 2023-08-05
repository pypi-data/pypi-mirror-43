from imageatm.handlers.data_generator import TrainDataGenerator, ValDataGenerator

TEST_CONFIG = {"batch_size": 8, "n_classes": 2}


def test__train_data_generator():
    generator = TrainDataGenerator(
        'samples_train',
        'image_dir',
        TEST_CONFIG['batch_size'],
        TEST_CONFIG['n_classes'],
        'preprocess_input',
    )

    assert generator.samples == 'samples_train'
    assert generator.img_dir == 'image_dir'
    assert generator.batch_size == 8
    assert generator.n_classes == 2
    assert generator.basenet_preprocess == 'preprocess_input'
    assert generator.img_load_dims == (256, 256)
    assert generator.img_crop_dims == (224, 224)
    assert generator.train == True

    assert generator.__len__() == 2


def test__val_data_generator():
    generator = ValDataGenerator(
        'samples_val',
        'image_dir',
        TEST_CONFIG['batch_size'],
        TEST_CONFIG['n_classes'],
        'preprocess_input',
    )

    assert generator.samples == 'samples_val'
    assert generator.img_dir == 'image_dir'
    assert generator.batch_size == 8
    assert generator.n_classes == 2
    assert generator.basenet_preprocess == 'preprocess_input'
    assert generator.img_load_dims == (224, 224)
    assert generator.train == False
    assert not hasattr(generator, 'img_crop_dims')

    assert generator.__len__() == 2
