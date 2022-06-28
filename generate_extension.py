#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Module to build a new extension.
"""

import os
import logging
import tempfile
from shutil import copytree, ignore_patterns, make_archive, copy
import xml.etree.ElementTree as ET
from make.addon import AddonUi


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('post_gen_project')

VERSION = "0.7.3-uni"
EXTENSION_NAME= "rdt_tools"
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
        '*.pyc', '*.py~', '__pycache__', '.idea',))


def generate_addons():
    """
    Addons are generated from a conf file located in make/
        - addon_ui.yml

    :return:
    """
    addon = AddonUi()
    with open("src/Addon.xcu", 'wb') as f:
        f.write(addon.doc.toprettyxml(encoding='UTF-8'))


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

    copy(extension_path, "/home/bastien/Bureau")
    return 1


if __name__ == '__main__':
    update_version()
    generate_addons()
    zip_files()
