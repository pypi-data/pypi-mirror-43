# Image ATM (Automated Tagging Machine)
The Image ATM system is a one-click tool that automates the workflow of a typical image classification pipeline, this includes:

- preprocessing and validating input images and labels
- starting/terminating cloud instance with GPU support
- training
- model evaluation

For more details see the [Image ATM confluence page](https://confluence.eu.idealo.com/pages/viewpage.action?pageId=209962715).


## Set up conda environment
```
conda env create -f environment.yml
conda activate image-atm
```

## Testing
Run `pytest -vs src/tests`

## Building
Run `python setup.py install`

## Command line client
To see all available options and commands run
```
image-atm --help
```

Each component can be run individually or a pipeline can be run, which then checks in the config file which components to run.


## TODOs:

- we are currently using Keras 2.2. The plan is to use tf.keras once TF 2.0 is out. Currently tf.keras is buggy,
  especially with model saving/loading (https://github.com/tensorflow/tensorflow/issues/22697)
