import os
import argparse
from imageatm.components import Training


def run_training(image_dir, job_dir, **kwargs):
    trainer = Training(image_dir, job_dir, **kwargs)
    trainer.train()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--job-dir', help='Directory with job files.', required=True)
    parser.add_argument('-i', '--image-dir', help='Directory with image files.', required=True)
    parser.add_argument('--batch-size', help='Batch size.', required=False)
    parser.add_argument(
        '--epochs-train-dense', help='Number of epochs train only dense layer.', required=False
    )
    parser.add_argument(
        '--epochs-train-all', help='Number of epochs train all layers.', required=False
    )
    parser.add_argument('--learning-rate-dense', help='Learning rate dense layers.', required=False)
    parser.add_argument('--learning-rate-all', help='Learning rate all layers.', required=False)
    args = parser.parse_args()

    run_training(**{**args.__dict__, **os.environ})
