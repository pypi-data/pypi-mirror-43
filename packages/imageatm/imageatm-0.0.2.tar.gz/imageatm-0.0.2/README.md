# Image ATM (Automated Tagging Machine)

Image ATM is a one-click tool that automates the workflow of a typical image classification pipeline in an opinionated way, this includes:

- Preprocessing and validating input images and labels
- Starting/terminating cloud instance with GPU support
- Training
- Model evaluation

## Getting Started
Run this from your terminal
```
imageatm pipeline config/config_file.yml
```

## Installation
There are two ways to install Image ATM:

* Install Image ATM from PyPI (recommended):
```
pip install imageatm
```

* Install Image ATM from the GitHub source:
```
git clone https://github.com/idealo/imageatm.git
cd imageatm
python setup.py install
```

## Testing
Run `pytest -vs tests`


## TODOs:

- We are currently using Keras 2.2. The plan is to use tf.keras once TF 2.0 is out. Currently tf.keras is buggy,
  especially with model saving/loading (https://github.com/tensorflow/tensorflow/issues/22697)

## Copyright

See [LICENSE](LICENSE) for details.
