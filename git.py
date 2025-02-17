import configparser
import os
import tools.os


def is_git_dir(path):
    if os.path.isdir(path):
        return tools.os.run(f"git rev-parse", "git rev-parse", path, None) == 0
    return False


def init_submodules(path, update=True):
    tools.os.run(f"git submodule init", "init-submodule", path)
    if update:
        update_submodules(path)


def update_submodules(path):
    tools.os.run(f"git submodule update --init --recursive", "update-submodule", path)


def checkout(path, tag):
    if is_git_dir(path):
        tools.os.run(f"git reset --hard", "reset", path)
        tools.os.run(f"git clean -fdx", "clean", path)
        tools.os.run(f"git checkout {tag}", "checkout", path)
        # tools.os.run(f"git pull", "pull", path)


def prepare_submodule(path):
    if is_git_dir(path):
        # tools.os.run(f"git reset --hard", "reset", path)
        # tools.os.run(f"git clean -fdx", "clean", path)
        # tools.os.run(f"git pull", "pull", path)

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
                d = {key: config[section][key] for key in config[section]}
                d["name"] = submodule_name
                submodules.append(d)

        return submodules

    return []


def bundle(path, outdir, name=None):
    path = os.path.abspath(path)
    outdir = os.path.abspath(outdir)

    if is_git_dir(path):
        init_submodules(path)
        old_cwd = os.getcwd()
        os.chdir(path)
        if name is None:
            name = os.path.basename(path)
        tools.os.run(f"git bundle create {name} --all", "bundle", path)
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        os.rename(name, os.path.join(outdir, name))
        os.chdir(old_cwd)
        return

    print(f"not a git repo: {path}")


def unbundle(path, outdir):
    path = os.path.abspath(path)
    outdir = os.path.abspath(outdir)
    print(f"unbundling {path} to {outdir}")

    if is_git_dir(outdir):
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        tools.os.run(f"git clone {path}", "unbundle", outdir)
        return

    print(f"not a git repo: {path}")


def bundle_submodules(path, outdir):
    if is_git_dir(path):
        for sm in submodules(path):
            bundle(os.path.join(path, sm["path"]), outdir)
        return
    print(f"not a git repo: {path}")


def unbundle_submodules(path, bundles):
    if is_git_dir(path):
        for sm in submodules(path):
            submodule_dir = os.path.abspath(os.path.join(path, sm["path"]))
            if len(os.listdir(submodule_dir)) == 0:
                submodule_name = os.path.basename(submodule_dir)
                bundle_path = os.path.abspath(os.path.join(bundles, submodule_name))
                unbundle(bundle_path, submodule_dir)
            else:
                print(f"not an empty directory: {submodule_dir}")
        return
    print(f"not a git repo: {path}")
