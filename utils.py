import os
import errno


def get_expanded_file_list(*files):
    file_lst = []

    for file in files:

        # Add file
        if os.path.isfile(file):
            file_lst.append(file)

        # Parse folder
        elif os.path.isdir(file):
            for path, subdirs, cfiles in os.walk(file):
                for name in cfiles:
                    file_path = os.path.join(path, name)[len(file):]  # Relative file path cropped
                    file_lst.append(file_path)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)

    return file_lst


