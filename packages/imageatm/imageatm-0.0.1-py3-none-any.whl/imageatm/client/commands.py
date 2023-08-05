import os
from imageatm.handlers.logger import get_logger
from imageatm.client.config import (
    validate_config,
    update_config,
    update_component_configs,
    config_set_image_dir,
    config_set_job_dir,
)


def pipeline(
    config,
    config_file,
    job_dir=None,
    image_dir=None,
    samples_file=None,
    provider=None,
    instance_type=None,
    region=None,
    vpc_id=None,
    bucket=None,
    tf_dir=None,
    train_cloud=None,
    destroy=None,
    resize=None,
    batch_size=None,
    learning_rate_dense=None,
    learning_rate_all=None,
    epochs_train_dense=None,
    epochs_train_all=None,
):
    '''Runs the entire pipeline based on config file.
    '''
    config = update_config(
        config=config,
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
        batch_size=batch_size,
        learning_rate_dense=learning_rate_dense,
        learning_rate_all=learning_rate_all,
        epochs_train_dense=epochs_train_dense,
        epochs_train_all=epochs_train_all,
    )
    config = config_set_image_dir(config)
    config = config_set_job_dir(config)
    config = update_component_configs(config)

    validate_config(config, config.pipeline)

    logger = get_logger(__name__, config.job_dir)

    if 'data_prep' in config.pipeline:
        from imageatm.scripts import run_data_prep

        logger.info(
            '\n********************************\n'
            '******* Data preparation *******\n'
            '********************************'
        )

        run_data_prep(**config.data_prep)

        # update image_dir if images were resized
        if config.data_prep.get('resize', False):
            config.image_dir = os.path.join(config.image_dir, '_resized')
            config = update_component_configs(config)

    if 'train' in config.pipeline:
        logger.info(
            '\n********************************\n'
            '*********** Training ***********\n'
            '********************************'
        )

        if config.train.get('cloud'):
            from imageatm.scripts import run_training_cloud

            run_training_cloud(**{**config.cloud, **config.train})
        else:
            from imageatm.scripts import run_training

            run_training(**config.train)

    if 'evaluate' in config.pipeline:
        from imageatm.scripts import run_evaluation

        logger.info(
            '\n********************************\n'
            '********** Evaluation **********\n'
            '********************************'
        )

        run_evaluation(**config.evaluate)

    if 'cloud' in config.pipeline:
        from imageatm.scripts import run_cloud

        run_cloud(**config.cloud)


def dataprep(config, config_file, image_dir, samples_file, job_dir, resize):
    config = update_config(
        config=config,
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


def train(
    config,
    config_file=None,
    job_dir=None,
    image_dir=None,
    provider=None,
    instance_type=None,
    region=None,
    vpc_id=None,
    bucket=None,
    tf_dir=None,
    train_cloud=None,
    destroy=None,
    batch_size=None,
    learning_rate_dense=None,
    learning_rate_all=None,
    epochs_train_dense=None,
    epochs_train_all=None,
):
    config = update_config(
        config=config,
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
        batch_size=batch_size,
        learning_rate_dense=learning_rate_dense,
        learning_rate_all=learning_rate_all,
        epochs_train_dense=epochs_train_dense,
        epochs_train_all=epochs_train_all,
    )

    config.train['run'] = True

    validate_config(config, ['train'])

    if config.train.get('cloud'):
        from imageatm.scripts import run_training_cloud

        run_training_cloud(**{**config.cloud, **config.train})
    else:
        from imageatm.scripts import run_training

        run_training(**config.train)


def evaluate(config, config_file=None, image_dir=None, job_dir=None):
    config = update_config(
        config=config, config_file=config_file, job_dir=job_dir, image_dir=image_dir
    )

    config.evaluate['run'] = True
    validate_config(config, ['evaluate'])

    from imageatm.scripts import run_evaluation

    run_evaluation(**config.evaluate)


def cloud(
    config,
    job_dir=None,
    config_file=None,
    provider=None,
    instance_type=None,
    region=None,
    vpc_id=None,
    bucket=None,
    tf_dir=None,
    train_cloud=None,
    destroy=None,
    no_destroy=None,
):
    config = update_config(
        config=config,
        job_dir=job_dir,
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
