import os
import multiprocessing
import tools.os
import tools.git


def do_install(src_path, install_path, options):
    tools.git.prepare_submodule(src_path)
    old_cwd = os.getcwd()
    os.chdir(src_path)

    joined_options = ' '.join([
        f'--prefix={install_path}'
    ] + options)

    tools.os.run(
        f'./autogen.sh {joined_options}',
        "generate"
    )
    tools.os.run(
        f'./configure {joined_options}',
        "configure"
    )
    tools.os.run(
        f"make -j{multiprocessing.cpu_count()}",
        "compile"
    )
    tools.os.run(
        f"make install",
        "install"
    )

    os.chdir(old_cwd)
