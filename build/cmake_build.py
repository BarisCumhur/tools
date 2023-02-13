import os
import multiprocessing


def do_install(src_path, build_path, install_path, options):
    if not os.path.isdir(build_path):
        os.makedirs(build_path)

    joined_options = ' '.join([
        '-DCMAKE_DEBUG_POSTFIX=d',
        f'-DCMAKE_INSTALL_PREFIX={install_path}'
    ] + options)

    old_cwd = os.getcwd()
    os.chdir(build_path)
    if os.system(f'cmake {src_path} {joined_options}') != 0:
        print("configuration failed")
        exit(-1)
    if os.system(f"cmake --build . --target install --config Debug --parallel {multiprocessing.cpu_count()}") != 0:
        print("install failed")
        exit(-1)
    if os.system(f"cmake --build . --target install --config Release --parallel {multiprocessing.cpu_count()}") != 0:
        print("install failed")
        exit(-1)

    os.chdir(old_cwd)
