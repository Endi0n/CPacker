import argparse

parser = argparse.ArgumentParser()

commands = parser.add_subparsers(title='commands', dest='command', required=True)
create_cmd = commands.add_parser('create')
create_cmd.add_argument('archive', help='the name of the archive to create')
create_cmd.add_argument('files', type=str,
                        nargs='+', help='the files to pack into the archive')

ls_cmd = commands.add_parser('list')
ls_cmd.add_argument('archive', help='the archive to list from')

unpack_cmd = commands.add_parser('unpack')
unpack_cmd.add_argument('archive', help='the archive to unpack')
unpack_cmd.add_argument('-o', metavar='DIR', help='output folder', default='./')
unpack_cmd.add_argument('--files', type=str,
                        nargs='+', help='the files to extract from the archive')

args = parser.parse_args()
