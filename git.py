

import os
import tools.os


def init_submodules(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    tools.os.run(f'git submodule init', "pull")
    tools.os.run(f'git submodule update --recursive', "pull")
    os.chdir(old_cwd)


def prepare_submodule(src_path):
    old_cwd = os.getcwd()
    os.chdir(src_path)
    tools.os.run(f'git reset --hard', "reset")
    os.chdir(old_cwd)

    init_submodules(src_path)
