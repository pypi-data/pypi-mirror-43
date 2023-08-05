from . import fontcell_main as fm
import os


def run(config_path):
    print('version: 1.0.7')
    conf = str(config_path.split('file:')[1])
    fm.fontcell(conf)
    return


def run_demo():
    # todo: make a executable demo for fusion of CELDA and Lifemap
    root_dir = os.path.dirname(os.path.realpath(__file__))
    proyect_path = root_dir + os.sep + 'fontcell_files'
    fm.fontcell(proyect_path + os.sep + 'demo_config.txt')
    print('output data at: ' + proyect_path + os.sep + 'results')
    return
