import os
import multiprocessing
import shutil


def do_install(deps_path, install_path):

    package_name = "boost"

    old_cwd = os.getcwd()
    os.chdir(f"{deps_path}/{package_name}")
    if not os.path.isfile("b2") and not os.path.isfile("b2.exe"):
        if os.system(f'bootstrap') != 0:
            print("bootstrap failed")
            exit(-1)
    else:
        shutil.rmtree("bin.v2")

    build_options = ' '.join([
        f'-s ZLIB_BINARY="{install_path}/bin"',
        f'-s ZLIB_INCLUDE="{install_path}/include"',
        f'-s ZLIB_LIBPATH="{install_path}/lib"',
        f'-s ZLIB_SOURCE="{deps_path}/zlib"',
        f'-j{multiprocessing.cpu_count()} ',
        f'--prefix={install_path}'
    ])

    if os.system(f"b2 headers {build_options}") != 0:
        print("build failed")
        exit(-1)
    if os.system(f"b2 install {build_options}") != 0:
        print("install failed")
        exit(-1)

    os.chdir(old_cwd)
