from imageatm.handlers.utils import load_yaml


def update_component_configs(config):
    '''
    Populate central parameters to component configs
    '''
    if config.image_dir:
        config.data_prep['image_dir'] = config.image_dir
        config.train['image_dir'] = config.image_dir
        config.evaluate['image_dir'] = config.image_dir

    if config.job_dir:
        config.data_prep['job_dir'] = config.job_dir
        config.train['job_dir'] = config.job_dir
        config.evaluate['job_dir'] = config.job_dir

    return config


def update_config(
    config,
    config_file=None,
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
    no_destroy=None,
    resize=None,
):
    # set defaults
    config.train['cloud'] = False
    config.data_prep['resize'] = False

    # load central config file
    if config_file:
        config_yml = load_yaml(config_file)

        # populate parameters from config file
        # parameters from config file overwrite defaults
        config.data_prep = {**config.data_prep, **config_yml.get('data_prep', {})}
        config.train = {**config.train, **config_yml.get('train', {})}
        config.evaluate = {**config.evaluate, **config_yml.get('evaluate', {})}
        config.cloud = {**config.cloud, **config_yml.get('cloud', {})}

        # set pipeline
        config.pipeline = [i for (i, j) in config_yml.items() if j.get('run')]

    # set options
    if job_dir:
        config.job_dir = job_dir

    if image_dir:
        config.image_dir = image_dir

    if samples_file:
        config.data_prep['samples_file'] = samples_file

    if provider:
        config.cloud['provider'] = provider

    if instance_type:
        config.cloud['instance_type'] = instance_type

    if region:
        config.cloud['region'] = region

    if vpc_id:
        config.cloud['vpc_id'] = vpc_id

    if bucket:
        config.cloud['bucket'] = bucket

    if tf_dir:
        config.cloud['tf_dir'] = tf_dir

    if train_cloud:
        config.train['cloud'] = train_cloud

    if destroy:
        config.cloud['destroy'] = destroy

    if no_destroy:
        config.cloud['destroy'] = False

    if resize:
        config.data_prep['resize'] = resize

    config = update_component_configs(config)

    return config


def get_diff(name, config, required_keys, optional_keys):
    allowed_keys = required_keys + optional_keys

    msg = []
    # check that all required keys are in config keys
    diff = list(set(required_keys).difference(config.keys()))
    if diff:
        msg.append('{} config: missing required parameters [{}]\n'.format(name, ', '.join(diff)))

    # check that config keys are in allowed keys
    diff = list(set(config.keys()).difference(allowed_keys))
    if diff:
        msg.append(
            '{} config: [{}] not in allowed parameters [{}]\n'.format(
                name, ', '.join(diff), ', '.join(allowed_keys)
            )
        )

    return msg


def val_data_prep(config):
    required_keys = ['image_dir', 'job_dir', 'samples_file', 'run']
    optional_keys = ['resize']

    return get_diff('data_prep', config, required_keys, optional_keys)


def val_train(config):
    required_keys = ['image_dir', 'job_dir', 'cloud', 'run']
    optional_keys = []

    return get_diff('train', config, required_keys, optional_keys)


def val_evaluate(config):
    required_keys = ['image_dir', 'job_dir', 'run']
    optional_keys = []

    return get_diff('evaluate', config, required_keys, optional_keys)


def val_cloud(config):
    allowed_providers = ['aws']

    assert config.get('provider') is not None, 'Config error: cloud config: missing provider'

    provider = config.get('provider')
    assert (
        provider in allowed_providers
    ), 'Config error: cloud config: {} not in allowed providers [{}]'.format(
        provider, *allowed_providers
    )

    required_keys = {
        'aws': [
            'run',
            'tf_dir',
            'region',
            'vpc_id',
            'instance_type',
            'bucket',
            'destroy',
            'provider',
        ]
    }
    optional_keys = []

    return get_diff('cloud', config, required_keys[provider], optional_keys)


def validate_config(config, components):
    msgs = []

    for component in components:
        config_component = getattr(config, component)

        if component == 'data_prep':
            msgs += val_data_prep(config_component)

        if component == 'train':
            msgs += val_train(config_component)

        if component == 'evaluate':
            msgs += val_evaluate(config_component)

        if component == 'cloud':
            msgs += val_cloud(config_component)

    assert len(msgs) == 0, '\nConfig error:\n{}'.format(''.join(msgs))
