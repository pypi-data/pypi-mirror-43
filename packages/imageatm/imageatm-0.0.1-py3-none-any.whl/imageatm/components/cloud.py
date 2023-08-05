import os
import time
from imageatm.handlers.utils import run_cmd
from imageatm.handlers.logger import get_logger


class AWS:
    def __init__(self, tf_dir, region, instance_type, vpc_id, s3_bucket, job_dir):
        self.tf_dir = tf_dir
        self.region = region
        self.instance_type = instance_type
        self.vpc_id = vpc_id
        self.s3_bucket = s3_bucket  # needed for IAM setup; bucket will not be created by terraform
        self.job_dir = os.path.abspath(job_dir)

        self.image_dir = None
        self.ssh = None
        self.remote_workdir = '/home/ec2-user/image-atm'

        self.__check_s3_prefix()

        self.logger = get_logger(__name__, self.job_dir)

    def __check_s3_prefix(self):
        # ensure that s3 bucket prefix is correct
        self.s3_bucket_wo = self.s3_bucket.split('s3://')[-1]  # without s3:// prefix
        self.s3_bucket = 's3://' + self.s3_bucket_wo

    def __set_ssh(self):
        cmd = 'cd {} && terraform output public_ip'.format(self.tf_dir)
        output = run_cmd(cmd, logger=self.logger, return_output=True)
        self.ssh = 'ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa ec2-user@{}'.format(output)

    def __set_remote_dirs(self):
        cmd = '{} mkdir -p {}'.format(self.ssh, self.remote_workdir)
        run_cmd(cmd, logger=self.logger)

        self.remote_image_dir = os.path.join(self.remote_workdir, os.path.basename(self.image_dir))
        self.remote_job_dir = os.path.join(self.remote_workdir, os.path.basename(self.job_dir))

    def __set_s3_dirs(self):
        if 's3://' in self.image_dir:
            self.s3_image_dir = self.image_dir
        else:
            self.s3_image_dir = os.path.join(
                self.s3_bucket, 'image_dirs', os.path.basename(self.image_dir)
            )

        if 's3://' in self.job_dir:
            self.s3_job_dir = self.job_dir
        else:
            self.s3_job_dir = os.path.join(
                self.s3_bucket, 'job_dirs', os.path.basename(self.job_dir)
            )

    def __sync_local_s3(self):
        self.logger.info('Syncing files local <> s3...')
        self.__set_s3_dirs()

        # only sync if image dir is local dir
        if 's3://' not in self.image_dir:
            cmd = 'aws s3 sync --quiet {} {}'.format(self.image_dir, self.s3_image_dir)
            run_cmd(cmd, logger=self.logger)

        # only sync if job dir is local dir
        if 's3://' not in self.job_dir:
            cmd = 'aws s3 sync --quiet {} {}'.format(self.job_dir, self.s3_job_dir)
            run_cmd(cmd, logger=self.logger)

    def __sync_s3_local(self):
        self.logger.info('Syncing files s3 <> local...')
        self.__set_s3_dirs()

        # only sync if job dir is local dir
        if 's3://' not in self.job_dir:
            cmd = 'aws s3 sync --quiet {} {}'.format(self.s3_job_dir, self.job_dir)
            run_cmd(cmd, logger=self.logger, level='info')

    def __sync_remote_s3(self):
        self.logger.info('Syncing files remote <> s3...')
        self.__set_s3_dirs()
        self.__set_remote_dirs()

        cmd = '{} aws s3 sync --quiet {} {}'.format(
            self.ssh, self.remote_image_dir, self.s3_image_dir
        )
        run_cmd(cmd, logger=self.logger)

        cmd = '{} aws s3 sync --quiet {} {}'.format(self.ssh, self.remote_job_dir, self.s3_job_dir)
        run_cmd(cmd, logger=self.logger)

    def __sync_s3_remote(self):
        self.logger.info('Syncing files s3 <> remote...')
        self.__set_s3_dirs()
        self.__set_remote_dirs()

        cmd = '{} aws s3 sync --quiet {} {}'.format(
            self.ssh, self.s3_image_dir, self.remote_image_dir
        )
        run_cmd(cmd, logger=self.logger)

        cmd = '{} aws s3 sync --quiet {} {}'.format(self.ssh, self.s3_job_dir, self.remote_job_dir)
        run_cmd(cmd, logger=self.logger)

    def __launch_train_container(self, **kwargs):
        self.logger.info('Launching training container...')
        # training parameters are passed to container through environment variables
        envs = ['-e {}={}'.format(key, value) for key, value in kwargs.items()]
        cmd = (
            '{} docker run -d -v {}:$WORKDIR/image_dir -v {}:$WORKDIR/job_dir {} '
            'idealo/tensorflow-image-atm:1.12.0'
        ).format(self.ssh, self.remote_image_dir, self.remote_job_dir, ' '.join(envs))
        run_cmd(cmd, logger=self.logger)

    def __stream_docker_logs(self):
        time.sleep(5)
        cmd = '{} docker ps -l -q'.format(self.ssh)
        output = run_cmd(cmd, logger=self.logger, return_output=True)

        cmd = '{} docker logs {} --follow'.format(self.ssh, output)
        run_cmd(cmd, logger=self.logger, level='info')

    def init(self):
        self.logger.info('Running terraform init...')
        cmd = 'cd {} && terraform init'.format(self.tf_dir)
        run_cmd(cmd, logger=self.logger)

    def apply(self):
        self.logger.info('Running terraform apply...')
        cmd = (
            'cd {} && terraform apply -auto-approve -var "region={}" -var "instance_type={}" '
            '-var "vpc_id={}" -var "s3_bucket={}"'
        ).format(self.tf_dir, self.region, self.instance_type, self.vpc_id, self.s3_bucket_wo)

        run_cmd(cmd, logger=self.logger)

        self.__set_ssh()

    def train(self, image_dir=None, job_dir=None, **kwargs):
        self.logger.info('Setting up remote instance...')
        if image_dir is not None:
            self.image_dir = os.path.abspath(image_dir)

        self.__sync_local_s3()
        self.__sync_s3_remote()
        self.__launch_train_container(**kwargs)
        self.__stream_docker_logs()
        self.__sync_remote_s3()
        self.__sync_s3_local()

    def destroy(self):
        self.logger.info('Running terraform destroy...')
        cmd = (
            'cd {} && terraform destroy -auto-approve -var "region={}" -var "instance_type={}" '
            '-var "vpc_id={}" -var "s3_bucket={}"'
        ).format(self.tf_dir, self.region, self.instance_type, self.vpc_id, self.s3_bucket_wo)

        run_cmd(cmd, logger=self.logger)
