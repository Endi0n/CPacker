import utils
import struct
import io


def archive_create(archive, files):
    g = open(archive, 'wb')

    g.write(b'\x99CPack')  # File signature
    g.write(struct.pack('>H', 0))  # CPack format version
    g.write(b'\x00' * 8)

    files_meta = []

    for file_name, file_path in utils.get_expanded_file_list(*files):
        tmp_file = open(file_path, 'rb')

        file_start = g.tell()

        g.write(tmp_file.read())

        file_end = g.tell()

        tmp_file.close()

        files_meta.append((file_name, file_start, file_end - file_start))

    footer_start = g.tell()

    for file_name, file_start, file_size in files_meta:
        g.write(struct.pack('H', len(file_name)))
        g.write(file_name.encode())

        g.write(struct.pack('L', file_start))
        g.write(struct.pack('L', file_size))

    g.seek(8, io.SEEK_SET)
    g.write(struct.pack('L', footer_start))

    g.close()


def archive_list(archive):
    f = open(archive, 'rb')

    signature = f.read(6)
    if signature != b'\x99CPack':
        raise ValueError('File is not an CPack archive')

    version = struct.unpack('>H', f.read(2))[0]
    if version != 0:
        raise ValueError('Unsupported CPack archive version')

    footer_start = struct.unpack('L', f.read(8))[0]
    f.seek(footer_start, io.SEEK_SET)

    while True:
        data = f.read(2)

        if not data:
            break

        file_name_size = struct.unpack('H', data)[0]
        file_name = f.read(file_name_size).decode()
        f.read(16)
        print(file_name)


def archive_unpack(archive, output_folder, files=None):
    print(archive, output_folder, files)

