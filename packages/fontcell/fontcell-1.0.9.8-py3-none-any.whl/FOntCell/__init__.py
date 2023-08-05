from . import fontcell_main as fm
import os
import shutil


def run(config_path, demo=False):
    print('version: 1.0.9.8')
    root_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.isdir(root_dir + os.sep + 'results'):
        os.mkdir(root_dir + os.sep + 'results')
    conf = str(config_path.split('file:')[1])
    fm.fontcell(conf, demo)
    return


def run_demo():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = root_dir + os.sep + 'fontcell_demo'
    run('file:' + project_path + os.sep + 'demo_configurations.txt', demo=True)
    print('output data at: ' + project_path + os.sep + 'results')
    return


def del_old_files():
    root_dir = os.path.dirname(os.path.realpath(__file__))
    project_path = root_dir + os.sep + 'fontcell_files'
    try:
        shutil.rmtree(project_path)
        print('old files deleted')
    except:
        print('There is no internal files yet')
    return
