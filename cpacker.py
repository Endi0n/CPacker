import argparse
import commands

parser = argparse.ArgumentParser()

commands_arg = parser.add_subparsers(title='commands', dest='command', required=True)
create_cmd = commands_arg.add_parser('create')
create_cmd.add_argument('archive', help='the name of the archive to create')
create_cmd.add_argument('files', type=str,
                        nargs='+', help='the files to pack into the archive')

ls_cmd = commands_arg.add_parser('list')
ls_cmd.add_argument('archive', help='the archive to list from')

unpack_cmd = commands_arg.add_parser('unpack')
unpack_cmd.add_argument('archive', help='the archive to unpack')
unpack_cmd.add_argument('-o', metavar='DIR', dest='output_folder', help='output folder')
unpack_cmd.add_argument('--files', type=str,
                        nargs='+', help='the files to extract from the archive')

args = parser.parse_args()
args_command = args.command

args_args = vars(args)
del args_args['command']  # Remove additional parameter

# Dispatch table
COMMAND_HANDLER_MAP = {
    'create': commands.archive_create,
    'list': commands.archive_list,
    'unpack': commands.archive_unpack,
}

# Invocation
COMMAND_HANDLER_MAP[args_command](**args_args)
