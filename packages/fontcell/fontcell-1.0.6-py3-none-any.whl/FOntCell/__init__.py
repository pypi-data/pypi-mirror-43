from . import fontcell_main as fm
import os


def run(config_path):
    print('version: 1.0.6')
    conf = str(config_path.split('file:')[1])
    fm.fontcell(conf)
    return

