#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copyspecial Assignment"""

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import re
import os
import shutil
import subprocess
import argparse
import sys


__author__ = "Janell.Huyck with help from madarp"


# Write functions and modify main() to call them
def get_special_paths(directory):
    """Return a list of the absolute paths of the
    special files in the given directory"""

    file_list = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_list.append(os.path.join(root, name))

    special_files = filter(lambda file: re.search(r'__\w+__', file), file_list)
    special_files = [os.path.abspath(filename) for filename in special_files]
    return special_files


def copy_to(special_paths, dir):
    """Given a list of paths, copy those files
    into the given directory."""

    for source_path in special_paths:
        filename = os.path.basename(source_path)
        destination_path = os.path.join(dir, filename)
        destination_path = os.path.abspath(destination_path)

        if not os.path.exists(dir):
            os.makedirs(dir)

        try:
            shutil.copyfile(source_path, destination_path)
        except shutil.Error as e:
            print("Unable to copy files.  Error message: {}".format(e))


def zip_to(paths, new_file):
    """Given a list of paths, zip those files up
    into the given zipfile"""

    cmd = ['zip', '-j', new_file]
    cmd.extend(paths)
    # leaving this print statement in per assignment instructions
    print("About to execute this command: ", str(cmd))
    subprocess.run(cmd)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--todir', help='dest dir for special files')
    parser.add_argument('--tozip', help='dest zipfile for special files')
    parser.add_argument(
        'fromdir', help='origin directory for special files')
    args = parser.parse_args()

    if not args:
        parser.print_usage()
        sys.exit(1)

    return args


def main():
    args = parse_args()

    special_paths = get_special_paths(args.fromdir)

    if args.todir:
        copy_to(special_paths, args.todir)
    elif args.tozip:
        zip_to(special_paths, args.tozip)
    else:
        for file in special_paths:
            print(file,)


if __name__ == "__main__":
    main()
