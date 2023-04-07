

import os
import tools.os


def prepare_submodule(src_path):
    old_cwd = os.getcwd()
    os.chdir(src_path)
    tools.os.run(
        f'git reset --hard',
        "reset"
    )
    tools.os.run(
        f'git pull',
        "pull"
    )
    tools.os.run(
        f'git submodule init',
        "pull"
    )
    tools.os.run(
        f'git submodule update --recursive',
        "pull"
    )
    os.chdir(old_cwd)
