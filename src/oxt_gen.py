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
VERSION = "0.0.2"
EXTENSION_NAME= "tcm"
OUTPUT = 'extension'


def update_version():
    update_description_version()
    # update_addon_ui()


def update_description_version():
    description_file = 'src/description.xml'
    tree = ET.parse(description_file)
    root = tree.getroot()
    # we suppose posisiton of version node won't change
    root[1].attrib['value'] = VERSION
    tree.write(description_file)


def update_addon_ui():
    addon_ui = 'src/AddonUI.xcu'
    with open(addon_ui, 'r') as f:
        content = f.read()
    content = re.sub(f"{EXTENSION_NAME}-[\d.]+", f"{EXTENSION_NAME}-{VERSION}.", content)
    with open(addon_ui, 'w') as f:
        f.write(content)


def create_tmp_src(temp_dir):
    copytree('src/', temp_dir, ignore=ignore_patterns(
        '*.pyc', '*.py~', '__pycache__', '.idea',
        'oxt_gen.py', 'README.md'
    ))


def zip_files():
    filename = f'{EXTENSION_NAME}-{VERSION}.oxt'
    msg = f'Zipping files to {filename}'
    logger.info(msg)
    extension_path = os.path.join(OUTPUT, filename)
    with tempfile.TemporaryDirectory() as tmpdirname:
        src = os.path.join(tmpdirname, 'src')
        create_tmp_src(src)
        make_archive(extension_path, 'zip', src)
        # os.rename(extension_path + '.zip', extension_path)
    return 1


if __name__ == '__main__':
    update_version()
    zip_files()
