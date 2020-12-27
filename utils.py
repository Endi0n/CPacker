import os
import errno
import math
import struct


def check_cpacker_file(file):
    signature = file.read(6)
    if signature != b'\x99CPack':
        raise ValueError('File is not an CPack archive')

    version = struct.unpack('>H', file.read(2))[0]
    if version != 0:
        raise ValueError('Unsupported CPack archive version')


def get_cpacker_file_list(file):
    files = []

    while True:
        data = file.read(2)

        if not data:
            break

        file_name_size = struct.unpack('H', data)[0]
        file_name = file.read(file_name_size).decode()

        file_start = struct.unpack('L', file.read(8))[0]
        file_size = struct.unpack('L', file.read(8))[0]

        files.append((file_name, file_start, file_size))

    return files


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
                    relative_file_path = file_path[len(os.getcwd()) + 1:]
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
