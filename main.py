#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from zipfile import ZipFile
from configparser import ConfigParser, ParsingError
from pathlib import Path, PurePath
from shutil import copy, rmtree
from time import sleep


# disable auto Uppercase
class MyConf(ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optionxform(self, optionstr):
        return optionstr


# load path from config file, disables unavailable keys
def load(cfg_file: PurePath):
    global workshop, modpath
    workshop, modpath = None, None
    changed = 0
    config = MyConf()
    try:
        config.read(cfg_file)
    except ParsingError as e:
        print('ERROR: ini file contains invalid content:', e.errors[0])
        exit(1)
    if 'global' not in config.sections():
        config['global'] = {'enabled': '1', 'workshop': '', 'modpath': ''}
        changed = 1
    if 'mod' not in config.sections():
        config['mod'] = {}
        changed = 1
    if 'workshop' in config.options('global') and config['global']['workshop'] != '':
        workshop = Path(config['global']['workshop'])
    if 'modpath' in config.options('global') and config['global']['modpath'] != '':
        modpath = Path(config['global']['modpath'])
    if workshop is not None:
        for file in workshop.glob('*/*.zip'):
            opt = r'%s\%s' % (file.parent.name, file.name)
            if opt not in config.options('mod') or config['mod'][opt] == '-2':
                changed = 1
                config['mod'][opt] = '0'  # Do Nothing
        for opt in config.options('mod'):
            if not workshop.joinpath(opt).is_file():
                changed = 1
                config['mod'][opt] = '-2'  # Not Exist
    if changed:
        with open(cfg_file, 'w') as f:
            print('File config.ini updated')
            config.write(f)
    return config


def unzip(file: PurePath):
    name = file.stem
    z = ZipFile(file)
    z.extractall(modpath / name)


# change the content of .mod file
def change(name: str):
    mod_file = modpath / (name + '.mod')
    copy(modpath / name / 'descriptor.mod', mod_file)
    content = mod_file.read_text()
    content = content.replace(r'archive="%s.zip"' % name, r'path="mod/%s"' % name)
    mod_file.write_text(content)


# remove the mod files in the 'modpath' which key is set to -1
def remove(name: str):
    found = False
    if modpath.joinpath(name + '.mod').is_file():
        modpath.joinpath(name + '.mod').unlink()
        found = True
    if (modpath / name).is_dir():
        rmtree(modpath / name)
        found = True
    if found:
        print('done')
    else:
        print('not found')


def main():
    cfg_file = Path(__file__).parent.joinpath('config.ini')
    config = load(cfg_file)
    if workshop is None or modpath is None:
        print('Please specify workshop and modpath in config.ini')
    else:
        print('config.ini loaded')
        if config['global']['enabled'] == '0':
            print('enabled = 0, wont work')
        else:
            for item in config.items('mod'):
                if item[1] == '1':  # Extract
                    print('Extracting %s ...' % item[0], end='', flush=True)
                    unzip(workshop.joinpath(item[0]))
                    change(Path(item[0]).stem)
                    print('done')
                elif item[1] == '-1':  # Remove
                    print('removing %s ...' % Path(item[0]).stem, end='', flush=True)
                    remove(Path(item[0]).stem)
    print('\nAuto exit in 3 seconds...')
    sleep(3)
    return


if __name__ == '__main__':
    main()
