import os
import click
from imageatm.handlers.config import validate_config, update_config, update_component_configs


# config object is passed from group parent to subcommand
class Config:
    def __init__(self):
        # components
        self.data_prep = {}
        self.train = {}
        self.cloud = {}
        self.evaluate = {}

        # central parameters
        self.image_dir = None
        self.job_dir = None

        self.pipeline = None


# creates config object that will be passed from cli to subcommands
pass_config = click.make_pass_decorator(Config, ensure=True)


# cli is the group parent, it gets run before any of the subcommands are run
@click.group()
@pass_config
def cli(config):
    pass


@cli.command()
@click.argument('config-file', type=click.Path())
@click.option('--image-dir', type=click.Path(), help='Directory with image files.')
@click.option('--samples-file', type=click.Path(), help='JSON file with samples.')
@click.option(
    '--job-dir',
    type=click.Path(),
    help=('Directory with train, val, and test samples files and class_mapping file.'),
)
@click.option('--provider', help='Cloud provider, currently supported: [aws].')
@click.option('--instance-type', help='Cloud instance_type [aws].')
@click.option('--region', help='Cloud region [aws].')
@click.option('--vpc-id', help='Cloud VPC id [aws].')
@click.option('--bucket', help='Cloud bucket used for persistence [aws].')
@click.option('--tf-dir', help='Directory with Terraform configs [aws].')
@click.option('--train-cloud', is_flag=True, required=False, help='Run training in cloud [aws].')
@click.option('--destroy', is_flag=True, required=False, help='Destroys cloud.')
@click.option('--resize', is_flag=True, required=False, help='Resizes images in data_prep.')
@pass_config
def pipeline(
    config,
    config_file,
    job_dir,
    image_dir,
    samples_file,
    provider,
    instance_type,
    region,
    vpc_id,
    bucket,
    tf_dir,
    train_cloud,
    destroy,
    resize,
):
    '''Runs all components for which run=True in config file.

    All activated (run=True) components from config file will be run in sequence. Options overwrite the config file.
    The config file is the only way to define pipeline components.

    Args:
        config-file: Central configuration file.
    '''

    config = update_config(
        config,
        config_file=config_file,
        job_dir=job_dir,
        image_dir=image_dir,
        samples_file=samples_file,
        provider=provider,
        instance_type=instance_type,
        region=region,
        vpc_id=vpc_id,
        bucket=bucket,
        tf_dir=tf_dir,
        train_cloud=train_cloud,
        destroy=destroy,
        resize=resize,
    )

    # set job_dir if not already set by client option
    if config.job_dir is None:
        if config.data_prep.get('job_dir') and config.data_prep.get('run'):
            config.job_dir = config.data_prep.get('job_dir')

        elif config.train.get('job_dir') and config.train.get('run'):
            config.job_dir = config.train.get('job_dir')

        elif config.evaluate.get('job_dir') and config.evaluate.get('run'):
            config.job_dir = config.evaluate.get('job_dir')

    # set image_dir if not already set by client option
    if config.image_dir is None:
        if config.data_prep.get('image_dir') and config.data_prep.get('run'):
            config.image_dir = config.data_prep.get('image_dir')

        elif config.train.get('image_dir') and config.train.get('run'):
            config.image_dir = config.train.get('image_dir')

        elif config.evaluate.get('image_dir') and config.evaluate.get('run'):
            config.image_dir = config.evaluate.get('image_dir')

    config = update_component_configs(config)

    validate_config(config, config.pipeline)

    if 'data_prep' in config.pipeline:
        from imageatm.scripts import run_data_prep

        run_data_prep(**config.data_prep)

        # update image_dir if images were resized
        if config.data_prep.get('resize', False):
            config.image_dir = os.path.join(config.image_dir, '_resized')
            config = update_component_configs(config)

    if 'train' in config.pipeline:
        if config.train.get('cloud'):
            from imageatm.scripts import run_training_cloud

            run_training_cloud(**config.train, **config.cloud)
        else:
            from imageatm.scripts import run_training

            run_training(**config.train)

    if 'evaluate' in config.pipeline:
        from imageatm.scripts import run_evaluation

        run_evaluation(**config.evaluate)


@cli.command()
@click.option('--config-file', type=click.Path(), help='Central configuration file.')
@click.option('--image-dir', type=click.Path(), help='Directory with image files.')
@click.option('--samples-file', type=click.Path(), help='JSON file with samples.')
@click.option(
    '--job-dir',
    type=click.Path(),
    help=('Directory with train, val, and test samples files and class_mapping file.'),
)
@click.option(
    '--resize',
    is_flag=True,
    required=False,
    help='Resizes images and stores them in _resized subfolder.',
)
@pass_config
def dataprep(config, config_file, image_dir, samples_file, job_dir, resize):
    '''Run data preparation and create job dir.

    Creates a directory (job_dir) with the following files:

        - train_samples.json

        - val_samples.json

        - test_samples.json

        - class_mapping.json
    '''
    config = update_config(
        config,
        config_file=config_file,
        job_dir=job_dir,
        image_dir=image_dir,
        samples_file=samples_file,
        resize=resize,
    )

    config.data_prep['run'] = True
    validate_config(config, ['data_prep'])

    from imageatm.scripts import run_data_prep

    run_data_prep(**config.data_prep)


@cli.command()
@click.option('--config-file', type=click.Path(), help='Central configuration file.')
@click.option('--image-dir', type=click.Path(), help='Directory with image files.')
@click.option(
    '--job-dir',
    type=click.Path(),
    help=('Directory with train, val, and test samples files and class_mapping file.'),
)
@click.option('--provider', help='Cloud provider, currently supported: [aws].')
@click.option('--instance-type', help='Cloud instance_type [aws].')
@click.option('--region', help='Cloud region [aws].')
@click.option('--vpc-id', help='Cloud VPC id [aws].')
@click.option('--bucket', help='Cloud bucket used for persistence [aws].')
@click.option('--tf-dir', help='Directory with Terraform configs [aws].')
@click.option('--train-cloud', is_flag=True, required=False, help='Run training in cloud [aws].')
@click.option('--destroy', is_flag=True, required=False, help='Destroys cloud.')
@pass_config
def train(
    config,
    config_file,
    job_dir,
    image_dir,
    provider,
    instance_type,
    region,
    vpc_id,
    bucket,
    tf_dir,
    train_cloud,
    destroy,
):
    '''Train a CNN.

    Fine-tunes an ImageNet pre-trained CNN. The number of classes are derived from train_samples.json.
    After each epoch the model will be evaluated on val_samples.json.

    The best model (based on valuation accuracy) will be saved.

    Args:
        image_dir: Directory with image files.
        job_dir: Directory with train_samples, val_samples, and class_mapping.json.

    '''
    config = update_config(
        config,
        config_file=config_file,
        job_dir=job_dir,
        image_dir=image_dir,
        provider=provider,
        instance_type=instance_type,
        region=region,
        vpc_id=vpc_id,
        bucket=bucket,
        tf_dir=tf_dir,
        train_cloud=train_cloud,
        destroy=destroy,
    )

    config.train['run'] = True

    validate_config(config, ['train'])

    if config.train.get('cloud'):
        from imageatm.scripts import run_training_cloud

        run_training_cloud(**config.train, **config.cloud)
    else:
        from imageatm.scripts import run_training

        run_training(**config.train)


@cli.command()
@click.option('--config-file', type=click.Path(), help='Central configuration file.')
@click.option('--image-dir', type=click.Path(), help='Directory with image files.')
@click.option(
    '--job-dir', type=click.Path(), help=('Directory with test samples files and trained model.')
)
@pass_config
def evaluate(config, config_file, image_dir, job_dir):
    '''Evaluate a trained model.

    Evaluation will be performed on test_samples.json.

    Args:
        image_dir: Directory with image files.
        job_dir: Directory with test_samples.json and class_mapping.json.
    '''

    config = update_config(config, config_file=config_file, job_dir=job_dir, image_dir=image_dir)

    config.evaluate['run'] = True
    validate_config(config, ['evaluate'])

    from imageatm.scripts import run_evaluation

    run_evaluation(**config.evaluate)


@cli.command()
@click.option('--config-file', type=click.Path(), help='Central configuration file.')
@click.option('--provider', help='Cloud provider, currently supported: [aws].')
@click.option('--instance-type', help='Cloud instance_type [aws].')
@click.option('--region', help='Cloud region [aws].')
@click.option('--vpc-id', help='Cloud VPC id [aws].')
@click.option('--bucket', help='Cloud bucket used for persistence [aws].')
@click.option('--tf-dir', help='Directory with Terraform configs [aws].')
@click.option('--train-cloud', is_flag=True, required=False, help='Run training in cloud [aws].')
@click.option('--destroy', is_flag=True, required=False, help='Destroys cloud.')
@click.option('--no-destroy', is_flag=True, required=False, help='Keeps cloud.')
@pass_config
def cloud(
    config,
    config_file,
    provider,
    instance_type,
    region,
    vpc_id,
    bucket,
    tf_dir,
    train_cloud,
    destroy,
    no_destroy,
):
    '''Launch/destroy a cloud compute instance.

    Launch/destroy cloud instances with Terraform based on Terraform files in tf_dir.
    '''

    config = update_config(
        config,
        config_file=config_file,
        provider=provider,
        instance_type=instance_type,
        region=region,
        vpc_id=vpc_id,
        bucket=bucket,
        tf_dir=tf_dir,
        train_cloud=train_cloud,
        destroy=destroy,
        no_destroy=no_destroy,
    )

    config.cloud['run'] = True
    validate_config(config, ['cloud'])

    from imageatm.scripts import run_cloud

    run_cloud(**config.cloud)
