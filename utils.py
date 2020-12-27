import os
import errno
import math


def get_expanded_file_list(*files):
    file_lst = []

    for file in files:

        # Add file
        if os.path.isfile(file):
            file_lst.append((file, os.path.realpath(file)))

        # Parse folder
        elif os.path.isdir(file):
            for path, subdirs, cfiles in os.walk(file):
                for name in cfiles:
                    file_path = os.path.realpath(os.path.join(path, name))
                    relative_file_path = file_path[len(os.getcwd()):]
                    file_lst.append((relative_file_path, file_path))
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)

    return file_lst


def fmt_binary_size(size):
    units = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB']

    unit = 0
    for unit in range(0, len(units)):
        if size < 1024:
            break
        size /= 1024.0

    size = int(math.ceil(size))

    return f'{size} {units[unit]}'
