import re
import sys
import json
import yaml
import tqdm
import subprocess
from multiprocessing import Pool, cpu_count


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(data, target_file):
    with open(target_file, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)


def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.load(f)


def parallelise(function, data):
    processes = cpu_count()
    pool = Pool(processes=processes)
    results = list(tqdm.tqdm(pool.imap(function, data), total=len(data)))
    pool.close()
    return results


def run_cmd(cmd, logger, level='debug', return_output=False):
    # filter out ANSI color and font formatting
    ansi_re = re.compile(r'\x1b\[[0-9;]*m')

    p = subprocess.Popen(
        cmd,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
        bufsize=1,
    )

    # stream process stdout to logger if available

    stdout = []
    line = ''
    while True:
        inchar = p.stdout.read(1)
        line += inchar

        if line[-1:] == '\n':
            new_line = re.sub(ansi_re, '', line[:-1])

            if level == 'debug':
                logger.debug(new_line)
            else:
                logger.info(new_line)

            stdout.append(new_line)
            line = ''

        if not inchar:
            sys.stdout.flush()
            break

    output, error = p.communicate()

    if error:
        logger.error(error, exc_info=True)
    if return_output:
        return stdout[-1]
