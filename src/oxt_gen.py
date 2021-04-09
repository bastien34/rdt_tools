#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This will create a new extension.
"""

import os
import logging
import tempfile
import re
from shutil import copytree, ignore_patterns, make_archive
import xml.etree.ElementTree as ET


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('post_gen_project')

VERSION = "0.3.5"
EXTENSION_NAME= "rdt_utils"
OUTPUT = 'extension'


def update_version():
    update_description_version()

def update_description_version():
    description_file = 'src/description.xml'
    tree = ET.parse(description_file)
    root = tree.getroot()
    # we suppose position of version node won't change
    root[1].attrib['value'] = VERSION
    tree.write(description_file)


def create_tmp_src(temp_dir):
    copytree('src/', temp_dir, ignore=ignore_patterns(
        '*.pyc', '*.py~', '__pycache__', '.idea',
        'oxt_gen.py', 'README.md'
    ))


def zip_files():
    filename = f'{EXTENSION_NAME}.oxt'
    msg = f'Zipping files to {filename}'
    logger.info(msg)
    extension_path = os.path.join(OUTPUT, VERSION, filename)
    with tempfile.TemporaryDirectory() as tmpdirname:
        src = os.path.join(tmpdirname, 'src')
        create_tmp_src(src)
        make_archive(extension_path, 'zip', src)
        os.rename(extension_path + '.zip', extension_path)
    return 1


if __name__ == '__main__':
    update_version()
    zip_files()
