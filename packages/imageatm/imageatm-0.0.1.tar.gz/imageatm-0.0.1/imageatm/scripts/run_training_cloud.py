import argparse
from imageatm.components import AWS


def run_training_cloud(
    image_dir, job_dir, provider, tf_dir, region, instance_type, vpc_id, bucket, destroy, **kwargs
):
    if provider == 'aws':
        cloud = AWS(
            tf_dir=tf_dir,
            region=region,
            instance_type=instance_type,
            vpc_id=vpc_id,
            s3_bucket=bucket,
            job_dir=job_dir,
        )

    cloud.init()
    cloud.apply()
    cloud.train(image_dir=image_dir, job_dir=job_dir, **kwargs)

    if destroy:
        cloud.destroy()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--job-dir', help='Directory with job files.', required=True)
    parser.add_argument('--image-dir', help='Directory with image files.', required=True)
    parser.add_argument('--provider', help='Cloud provider [aws].', required=True)
    parser.add_argument('--tf-dir', help='Directory with Terraform files.', required=True)
    parser.add_argument('--region', help='Cloud region.', required=True)
    parser.add_argument('--instance-type', help='Cloud instance type.', required=True)
    parser.add_argument('--vpc-id', help='Cloud vpc id [aws].', required=True)
    parser.add_argument('--bucket', help='Cloud storage.', required=True)
    parser.add_argument('--batch-size', help='Batch size.', required=False)
    parser.add_argument(
        '--destroy',
        help='Whether instance shopuld be terminated after training.',
        action='store_true',
        default=False,
        required=True,
    )
    parser.add_argument(
        '--epochs-train-dense', help='Number of epochs train only dense layer.', required=False
    )
    parser.add_argument(
        '--epochs-train-all', help='Number of epochs train all layers.', required=False
    )
    parser.add_argument('--learning-rate-dense', help='Learning rate dense layers.', required=False)
    parser.add_argument('--learning-rate-all', help='Learning rate all layers.', required=False)

    args = parser.parse_args()

    run_training_cloud(**args.__dict__)
