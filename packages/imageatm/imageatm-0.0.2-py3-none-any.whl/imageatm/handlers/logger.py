import logging
import os
import sys


def get_logger(name, job_dir):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # stream handler ensures that logging events are passed to stdout
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch_formatter = logging.Formatter('%(message)s')
        ch.setFormatter(ch_formatter)
        logger.addHandler(ch)

        # file handler ensures that logging events are passed to log file
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)

        fh = logging.FileHandler(filename=os.path.join(job_dir, 'logs'))
        fh.setLevel(logging.DEBUG)
        fh_formatter = logging.Formatter(
            '%(asctime)s - %(module)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

    return logger
