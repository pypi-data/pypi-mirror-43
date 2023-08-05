import os
from click.testing import CliRunner
from imageatm.handlers.client import cli, Config

TEST_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_configs', 'config_1.yml'
)

TEST_SAMPLES_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_samples', 'test_int_labels.json'
)

TEST_IMG_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_images', 'test_img_dir'
)

TEST_JOB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_job_dir')


def test_help():
    runner = CliRunner()

    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0

    result = runner.invoke(cli, ['pipeline', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(cli, ['dataprep', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(cli, ['train', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(cli, ['evaluate', '--help'])
    assert result.exit_code == 0

    result = runner.invoke(cli, ['cloud', '--help'])
    assert result.exit_code == 0


def test_options_available():
    runner = CliRunner()

    expected = 'Options:\n  --help  Show this message and exit.\n\nCommands'
    result = runner.invoke(cli, ['--help'])
    assert expected in result.stdout

    expected = (
        'Options:\n'
        '  --image-dir PATH      Directory with image files.\n'
        '  --samples-file PATH   JSON file with samples.\n'
        '  --job-dir PATH        Directory with train, val, and test samples files and\n'
        '                        class_mapping file.\n'
        '  --provider TEXT       Cloud provider, currently supported: [aws].\n'
        '  --instance-type TEXT  Cloud instance_type [aws].\n'
        '  --region TEXT         Cloud region [aws].\n'
        '  --vpc-id TEXT         Cloud VPC id [aws].\n'
        '  --bucket TEXT         Cloud bucket used for persistence [aws].\n'
        '  --tf-dir TEXT         Directory with Terraform configs [aws].\n'
        '  --train-cloud         Run training in cloud [aws].\n'
        '  --destroy             Destroys cloud.\n'
        '  --resize              Resizes images in data_prep.\n'
        '  --help                Show this message and exit.\n'
    )
    result = runner.invoke(cli, ['pipeline', '--help'])
    assert expected in result.stdout

    expected = (
        'Options:\n'
        '  --config-file PATH   Central configuration file.\n'
        '  --image-dir PATH     Directory with image files.\n'
        '  --samples-file PATH  JSON file with samples.\n'
        '  --job-dir PATH       Directory with train, val, and test samples files and\n'
        '                       class_mapping file.\n'
        '  --resize             Resizes images and stores them in _resized subfolder.\n'
        '  --help               Show this message and exit.\n'
    )
    result = runner.invoke(cli, ['dataprep', '--help'])
    assert expected in result.stdout

    expected = (
        'Options:\n'
        '  --config-file PATH    Central configuration file.\n'
        '  --image-dir PATH      Directory with image files.\n'
        '  --job-dir PATH        Directory with train, val, and test samples files and\n'
        '                        class_mapping file.\n'
        '  --provider TEXT       Cloud provider, currently supported: [aws].\n'
        '  --instance-type TEXT  Cloud instance_type [aws].\n'
        '  --region TEXT         Cloud region [aws].\n'
        '  --vpc-id TEXT         Cloud VPC id [aws].\n'
        '  --bucket TEXT         Cloud bucket used for persistence [aws].\n'
        '  --tf-dir TEXT         Directory with Terraform configs [aws].\n'
        '  --train-cloud         Run training in cloud [aws].\n'
        '  --destroy             Destroys cloud.\n'
        '  --help                Show this message and exit.\n'
    )
    result = runner.invoke(cli, ['train', '--help'])
    assert expected in result.stdout

    expected = (
        'Options:\n'
        '  --config-file PATH  Central configuration file.\n'
        '  --image-dir PATH    Directory with image files.\n'
        '  --job-dir PATH      Directory with test samples files and trained model.\n'
        '  --help              Show this message and exit.\n'
    )
    result = runner.invoke(cli, ['evaluate', '--help'])
    assert expected in result.stdout

    expected = (
        'Options:\n'
        '  --config-file PATH    Central configuration file.\n'
        '  --provider TEXT       Cloud provider, currently supported: [aws].\n'
        '  --instance-type TEXT  Cloud instance_type [aws].\n'
        '  --region TEXT         Cloud region [aws].\n'
        '  --vpc-id TEXT         Cloud VPC id [aws].\n'
        '  --bucket TEXT         Cloud bucket used for persistence [aws].\n'
        '  --tf-dir TEXT         Directory with Terraform configs [aws].\n'
        '  --train-cloud         Run training in cloud [aws].\n'
        '  --destroy             Destroys cloud.\n'
        '  --no-destroy          Keeps cloud.\n'
        '  --help                Show this message and exit.\n'
    )
    result = runner.invoke(cli, ['cloud', '--help'])
    assert expected in result.stdout
