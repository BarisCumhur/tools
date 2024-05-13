import os
import tools.os


def init_submodules(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    tools.os.run(f"git submodule init", "pull")
    tools.os.run(f"git submodule update --recursive", "pull")
    os.chdir(old_cwd)


def checkout(path, tag):
    if os.path.isdir(path):
        old_cwd = os.getcwd()
        os.chdir(path)
        tools.os.run(f"git reset --hard", "reset")
        tools.os.run(f"git clean -fdx", "clean")
        tools.os.run(f"git checkout {tag}", "checkout")
        tools.os.run(f"git pull", "pull")
        os.chdir(old_cwd)


def prepare_submodule(path):
    if os.path.isdir(path):
        old_cwd = os.getcwd()
        os.chdir(path)
        tools.os.run(f"git reset --hard", "reset")
        tools.os.run(f"git clean -fdx", "clean")
        tools.os.run(f"git pull", "pull")
        os.chdir(old_cwd)

        init_submodules(path)
