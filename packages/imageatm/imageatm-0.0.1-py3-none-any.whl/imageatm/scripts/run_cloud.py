from imageatm.components import AWS


def run_cloud(provider, tf_dir, region, instance_type, vpc_id, bucket, destroy, job_dir, **kwargs):
    if provider == 'aws':
        cloud = AWS(
            tf_dir=tf_dir,
            region=region,
            instance_type=instance_type,
            vpc_id=vpc_id,
            s3_bucket=bucket,
            job_dir=job_dir,
        )

    if destroy:
        cloud.destroy()

    else:
        cloud.init()
        cloud.apply()
