import os
import multiprocessing
import tools.os


def do_install(src_path, build_path, install_path, options):
    if not os.path.isdir(build_path):
        os.makedirs(build_path)

    joined_options = ' '.join([
        '-DCMAKE_DEBUG_POSTFIX=d',
        f'-DCMAKE_INSTALL_PREFIX={install_path}'
    ] + options)

    old_cwd = os.getcwd()
    os.chdir(build_path)
    tools.os.run(
        f'cmake {src_path} {joined_options}',
        "configuration"
    )
    tools.os.run(
        f"cmake --build . --target install --config Debug --parallel {multiprocessing.cpu_count()}",
        "debug install"
    )
    tools.os.run(
        f"cmake --build . --target install --config Release --parallel {multiprocessing.cpu_count()}",
        "release install"
    )

    os.chdir(old_cwd)


def package_exists(name, compiler_id='GNU'):
    return os.system(f'cmake --find-package -DNAME={name} -DCOMPILER_ID={compiler_id} -DLANGUAGE=CXX -DMODE=EXIST') == 0
