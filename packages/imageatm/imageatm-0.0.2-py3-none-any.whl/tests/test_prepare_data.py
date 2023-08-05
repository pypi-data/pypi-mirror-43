import os
from collections import Counter
from imageatm.components.prepare_data import DataPrep
from imageatm.handlers.utils import load_json

''' Files for test_valid_images'''
INVALID_IMG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_images', 'image_invalid.jpg'
)

VALID_IMG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_images', 'image_960x540.jpg'
)

''' Files for sample validation'''
TEST_STR_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_samples', 'test_str_labels.json'
)
TEST_INT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_samples', 'test_samples_int.json'
)
TEST_FILE_STR2INT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_samples', 'test_int_labels.json'
)

TEST_IMG_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_images', 'test_img_dir'
)

TEST_STR_FILE_CORRUPTED = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_samples', 'test_str_labels_corrupted.json'
)

dp = object.__new__(DataPrep)


def test_valid_images():
    expected = ['helmet_1.jpg', 'helmet_3.jpg', 'helmet_2.jpg', 'image_png.png']

    dp.image_dir = TEST_IMG_DIR
    dp.validate_images()

    assert dp.valid_image_ids == expected


def test_validate_samples():
    expected = load_json(TEST_STR_FILE)

    dp.image_dir = TEST_IMG_DIR
    dp.samples = load_json(TEST_STR_FILE)
    dp.min_class_size = 1
    dp.validate_samples()

    assert dp.samples == expected

    # exclude first 3 samples as they are corrupted
    expected = load_json(TEST_STR_FILE_CORRUPTED)[3:]

    dp.image_dir = TEST_IMG_DIR
    dp.samples = load_json(TEST_STR_FILE_CORRUPTED)
    dp.min_class_size = 1
    dp.validate_images()
    dp.validate_samples()

    assert dp.samples == expected


def test_get_class_mapping():
    dp.samples = load_json(TEST_STR_FILE)
    dp.get_class_mapping()
    expected = {0: 'left', 1: 'right'}
    assert dp.class_mapping == expected

    dp.samples = dp.samples[::-1]
    dp.get_class_mapping()
    expected = {0: 'left', 1: 'right'}
    assert dp.class_mapping == expected

    dp.samples = load_json(TEST_INT_FILE)
    print(dp.samples)
    dp.get_class_mapping()
    print(dp.class_mapping)
    expected = {0: 1, 1: 2}
    assert dp.class_mapping == expected

    dp.samples = dp.samples[::-1]
    dp.get_class_mapping()
    expected = {0: 1, 1: 2}
    assert dp.class_mapping == expected


def test_convert_label_to_int():
    dp.samples = load_json(TEST_STR_FILE)
    dp.convert_label_to_int()
    expected = load_json(TEST_FILE_STR2INT)

    assert dp.samples == expected


def test_split_samples_0():
    dp.samples = load_json(TEST_INT_FILE)
    dp.test_size = 0.2
    dp.val_size = 0.5

    dp.split_samples()

    assert len(dp.train_samples) == 12
    assert len(dp.val_samples) == 12
    assert len(dp.test_samples) == 6

    train_labels_count = Counter([i['label'] for i in dp.train_samples])
    val_labels_count = Counter([i['label'] for i in dp.val_samples])
    test_labels_count = Counter([i['label'] for i in dp.test_samples])

    assert train_labels_count[1] == 8
    assert train_labels_count[2] == 4

    assert val_labels_count[1] == 8
    assert val_labels_count[2] == 4

    assert test_labels_count[1] == 4
    assert test_labels_count[2] == 2


def test_split_samples_1():
    dp.samples = load_json(TEST_INT_FILE)
    dp.test_size = 0.2
    dp.val_size = 0.1

    dp.split_samples()

    assert len(dp.train_samples) == 21
    assert len(dp.val_samples) == 3
    assert len(dp.test_samples) == 6

    train_labels_count = Counter([i['label'] for i in dp.train_samples])
    val_labels_count = Counter([i['label'] for i in dp.val_samples])
    test_labels_count = Counter([i['label'] for i in dp.test_samples])

    assert train_labels_count[1] == 14
    assert train_labels_count[2] == 7

    assert val_labels_count[1] == 2
    assert val_labels_count[2] == 1

    assert test_labels_count[1] == 4
    assert test_labels_count[2] == 2
