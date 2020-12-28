import utils
import struct
import io
import os
import pathlib


def archive_create(archive, files):
    g = open(archive, 'wb')

    g.write(b'\x99CPack')  # File signature
    g.write(struct.pack('>H', 0))  # CPack format version
    g.write(b'\x00' * 8)

    files_meta = []

    print('Archive contents:\n')
    print('{:15}{}'.format('Size:', 'File Name:'))
    print('{:15}{}'.format('-----', '----------'))

    for file_name, file_path in utils.get_expanded_file_list(*files):
        tmp_file = open(file_path, 'rb')

        file_start = g.tell()

        g.write(tmp_file.read())

        file_end = g.tell()

        tmp_file.close()

        file_size = file_end - file_start

        files_meta.append((file_name, file_start, file_size))

        print(f'{utils.fmt_binary_size(file_size):15}{file_name}')

    footer_start = g.tell()

    for file_name, file_start, file_size in files_meta:
        g.write(struct.pack('H', len(file_name)))
        g.write(file_name.encode())

        g.write(struct.pack('L', file_start))
        g.write(struct.pack('L', file_size))

    g.seek(8, io.SEEK_SET)
    g.write(struct.pack('L', footer_start))

    g.seek(0, io.SEEK_END)
    print(f'\nTotal archive size: {utils.fmt_binary_size(g.tell())}.')

    g.close()


def archive_list(archive):
    f = open(archive, 'rb')

    utils.check_cpacker_file(f)

    footer_start = struct.unpack('L', f.read(8))[0]
    f.seek(footer_start, io.SEEK_SET)

    file_list = utils.get_cpacker_file_list(f)

    if file_list:
        print('Archive contents:\n')
        print('{:15}{}'.format('Size:', 'File Name:'))
        print('{:15}{}'.format('-----', '----------'))
    else:
        print('The archive is empty.')
        return

    for file_name, _, file_size in file_list:
        print(f'{utils.fmt_binary_size(file_size):15}{file_name}.')


def archive_unpack(archive, output_folder=None, files=None):
    if not output_folder:
        output_folder = os.getcwd()

    f = open(archive, 'rb')
    utils.check_cpacker_file(f)

    footer_start = struct.unpack('L', f.read(8))[0]
    f.seek(footer_start, io.SEEK_SET)

    file_list = utils.get_cpacker_file_list(f)

    if files:
        file_list = [file for file in file_list if file[0] in files]

    if file_list:
        print(f'Unpacking to {os.path.relpath(output_folder)}{os.path.sep}:\n')
        print('{:15}{}'.format('Size:', 'File Name:'))
        print('{:15}{}'.format('-----', '----------'))
    else:
        print('Nothing to unpack.')
        return

    total_size = 0

    for file_name, file_start, file_size in file_list:
        file_path = os.path.join(output_folder, file_name)
        pathlib.Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)

        f.seek(file_start)

        tmp_file = open(file_path, 'wb')
        tmp_file.write(f.read(file_size))
        tmp_file.close()

        total_size += file_size

        print(f'{utils.fmt_binary_size(file_size):15}{file_name}')

    print(f'\nUnpacked {utils.fmt_binary_size(total_size)}.')
