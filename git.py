import configparser
import os
import tools.os

def is_git_dir(path):
    if os.path.isdir(path):
        old_cwd = os.getcwd()
        os.chdir(path)
        result = os.system(f"git rev-parse")
        os.chdir(old_cwd)
        return result == 0
    return False

def init_submodules(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    tools.os.run(f"git submodule update --init --recursive", "pull")
    os.chdir(old_cwd)


def checkout(path, tag):
    if is_git_dir(path):
        old_cwd = os.getcwd()
        os.chdir(path)
        tools.os.run(f"git reset --hard", "reset")
        tools.os.run(f"git clean -fdx", "clean")
        tools.os.run(f"git checkout {tag}", "checkout")
        tools.os.run(f"git pull", "pull")
        os.chdir(old_cwd)


def prepare_submodule(path):
    if is_git_dir(path):
        old_cwd = os.getcwd()
        os.chdir(path)
        tools.os.run(f"git reset --hard", "reset")
        tools.os.run(f"git clean -fdx", "clean")
        tools.os.run(f"git pull", "pull")
        os.chdir(old_cwd)

        init_submodules(path)


def submodules(path):
    if is_git_dir(path):
        # Create a ConfigParser instance
        config = configparser.ConfigParser()
        # Preserve case sensitivity in keys
        config.optionxform = str

        # Read the .gitmodules file
        config.read("./.gitmodules")

        # Parse the submodule details
        submodules = []
        for section in config.sections():
            if section.startswith("submodule"):
                submodule_name = section.split('"')[1]  # Extract the submodule name
                d = {
                    key: config[section][key] for key in config[section]
                }
                d["name"] = submodule_name
                submodules.append(d)

        return submodules
    
    return []


def bundle(path, outdir):
    if is_git_dir(path):
        old_cwd = os.getcwd()
        os.chdir(path)
        init_submodules(path)
        name = os.path.basename(path)
        tools.os.run(f"git bundle create {name} --all", "bundle")
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        os.rename(name, os.path.join(outdir, name))
        os.chdir(old_cwd)

        
def bundle_submodules(path, outdir):
    if is_git_dir(path):
        for sm in submodules(path):
            bundle(os.path.join(path, sm['path']), outdir)
        