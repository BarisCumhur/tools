import os

SHELL_EXT = ".sh" if os.name == "posix" else ".bat"
EXE_EXT = "" if os.name == "posix" else ".exe"
LIST_SEP = ":" if os.name == "posix" else ";"
PATH_SEP = "/" if os.name == "posix" else "\\"


def run(cmd, description):
    if os.system(cmd) != 0:
        print(f"{description} failed")
        exit(-1)

    return True
