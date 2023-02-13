import os
import multiprocessing
import shutil
import tools.os


def do_install(deps_path, install_path):

    old_cwd = os.getcwd()
    os.chdir(f"{deps_path}/boost")
    if not os.path.isfile("b2.{tools.os.EXE_EXT}"):
        tools.os.run(
            f'.{tools.os.PATH_SEP}bootstrap{tools.os.SHELL_EXT}',
            "bootstrap"
        )
    else:
        shutil.rmtree("bin.v2")

    build_options = ' '.join([
        f'-s ZLIB_BINARY="{install_path}/bin"',
        f'-s ZLIB_INCLUDE="{install_path}/include"',
        f'-s ZLIB_LIBPATH="{install_path}/lib"',
        f'-j{multiprocessing.cpu_count()} ',
        f'--prefix={install_path}'
    ])

    tools.os.run(
        f".{tools.os.PATH_SEP}b2{tools.os.EXE_EXT} headers {build_options}",
        "build"
    )
    tools.os.run(
        f".{tools.os.PATH_SEP}b2{tools.os.EXE_EXT} install {build_options}",
        "install"
    )

    os.chdir(old_cwd)
