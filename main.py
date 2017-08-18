#!/usr/bin/env python
import gevent
import gevent.monkey as monkey
monkey.patch_all()

import argparse
import os
import re
import subprocess

from gevent.pool import Pool



REQUIREMENT_FILE_NAME_PATTERN = r'requirements.*\.txt'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('base_path',
                        help='Basepath to search for requirement files')
    return parser.parse_args()


def find_requirement_files(repo_path):
    for root, dirs, files in os.walk(repo_path):
        path = root.split(os.sep)
        for file in files:
            if re.search(REQUIREMENT_FILE_NAME_PATTERN, file):
                path_to_file = os.path.sep.join(path) + os.path.sep + file
                yield path_to_file


def get_packages(file_path):
    for line in open(file_path):
        if line:
            yield line.strip()


def get_license(package_name):
    print('Fetching license for {}'.format(package_name))
    args = ['yolk', '-M', package_name, '-f', 'license']
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    out, err = process.communicate()
    if err:
        print('Error getting license for {}: {}'.format(package_name, err))
        return 'UNKNOWN'
    return out.decode('utf8').strip() or 'UNKNOWN'


def run():
    args = parse_args()

    packages = set()

    for requirement_file in find_requirement_files(args.base_path):
        print('Processing file: {}'.format(requirement_file))
        packages.update(get_packages(requirement_file))

    packages = sorted(list(packages), key=lambda x: x.lower())

    print('Found {} packages:'.format(len(packages)))
    for package in packages:
        print('    {}'.format(package))

    print('Fetching license info from PyPi...')

    pool = Pool(10)

    licenses = pool.map(get_license, packages)

    output = zip(packages, licenses)
    for package, license in output:
        print('{:<40s} {}'.format(package, license))



if __name__ == '__main__':
    run()
