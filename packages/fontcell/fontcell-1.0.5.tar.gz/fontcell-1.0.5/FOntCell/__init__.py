from . import fontcell_main as fm
import os


def run(config_path):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    proyect_path = os.path.abspath(os.path.join(root_dir, os.pardir))
    print(proyect_path)
    print('version: 1.0.1')
    conf = str(config_path.split('file:')[1])
    # create a  files directory
    fm.fontcell(conf)
    return

