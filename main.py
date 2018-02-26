#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from zipfile import ZipFile
from configparser import ConfigParser, ParsingError
from pathlib import Path
from shutil import copy, rmtree


class MyConf(ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optionxform(self, optionstr):
        return optionstr


def load(cfg_file: Path):
    global workshop, modpath
    config = MyConf()
    try:
        config.read(cfg_file)
    except ParsingError as e:
        print('ERROR: ini file contains invalid content:', e.errors[0])
        exit(1)
    if 'mod' not in config.sections():
        config['mod'] = {}
    if 'global' not in config.sections():
        config['global'] = {'workshop': '', 'modpath': ''}
        workshop = None
        modpath = None
    elif config['global']['workshop'] != '' and config['global']['modpath'] != '':
        workshop = Path(config['global']['workshop'])
        modpath = Path(config['global']['modpath'])
    if workshop is not None:
        for file in list(workshop.glob('*/*.zip')):
            opt = r'%s\%s' % (file.parent.name, file.name)
            if opt not in config.options('mod'):
                config['mod'][opt] = '0'
        for opt in config.options('mod'):
            if not workshop.joinpath(opt).is_file():
                config['mod'][opt] = '-1'
    return config


def unzip(file: Path):
    name = file.stem
    z = ZipFile(file)
    z.extractall(modpath / name)


def change(name: str):
    mod_file = modpath / (name + '.mod')
    copy(modpath / name / 'descriptor.mod', mod_file)
    content = mod_file.read_text()
    content = content.replace(r'archive="%s.zip"' % name, r'path="mod/%s"' % name)
    mod_file.write_text(content)


def remove(name: str):
    if modpath.joinpath(name + '.mod').is_file():
        modpath.joinpath(name + '.mod').unlink()
    if modpath.joinpath(name).is_dir():
        rmtree(modpath / name)


def main():
    cfg_file = Path(__file__).parent.joinpath('config.ini')
    config = load(cfg_file)
    if workshop is not None and modpath is not None:
        for item in config.items('mod'):
            if item[1] == '1':
                unzip(workshop.joinpath(item[0]))
                change(Path(item[0]).stem)
            elif item[1] == '-1':
                remove(Path(item[0]).stem)
    with open(cfg_file, 'w') as f:
        config.write(f)


if __name__ == '__main__':
    workshop = None
    modpath = None
    main()
