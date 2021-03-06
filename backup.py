import os
import shutil
import datetime


def _get_backup_path(path):
    return path.replace(DATA_DIR, BACKUP_DIR)


def _get_data_path(path):
    return path.replace(BACKUP_DIR, DATA_DIR)


def backup_files(from_path, to_path, max_size):
    print 'Creating backup at', datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')
    global DATA_DIR, BACKUP_DIR, MAX_FILE_SIZE
    DATA_DIR = from_path
    BACKUP_DIR = to_path
    MAX_FILE_SIZE = max_size

    # By default, this ignores hidden files and directories (beginning with .)
    skipped_files = []
    for (dirpath, dirnames, filenames) in os.walk(DATA_DIR):
        # If the current folder is hidden, ignore it
        if '.' in dirpath:
            pass
        else:
            backup_path = _get_backup_path(dirpath)
            if not os.path.exists(backup_path):
                os.mkdir(backup_path)
            for filename in filenames:
                source_path = os.sep.join([dirpath, filename])
                dest_path = os.sep.join([backup_path, filename])
                # rsync incrementally creates a backup
                # which is a better option than copying entire files again
                if os.path.getsize(source_path) <= MAX_FILE_SIZE:
                    if os.path.exists(dest_path):
                        # If a new version of the file is present, overwrite the old backup
                        if os.path.getmtime(source_path) > os.path.getmtime(dest_path):
                            print 'Updating backup of', source_path
                            # shutil.copyfile(source_path, dest_path)
                            os.system('rsync "{}" "{}"'.format(source_path, dest_path))
                    else:
                        # If the file does not exist, create a backup
                        print 'Creating backup of', source_path
                        # shutil.copyfile(source_path, dest_path)
                        os.system('rsync "{}" "{}"'.format(source_path, dest_path))
                else:
                    skipped_files.append(source_path + '\n')
                    print 'File is too big - skipping', source_path

    # Remove deleted files
    for (dirpath, dirnames, filenames) in os.walk(BACKUP_DIR):
        data_dir = _get_data_path(dirpath)
        # If the folder has been removed, delete it from the backup
        if not os.path.exists(data_dir):
            print 'Removing folder', dirpath
            shutil.rmtree(dirpath)
        else:
            # If the outer folder has not been deleted, check the files inside it
            for filename in filenames:
                backup_path = os.sep.join([dirpath, filename])
                source_path = os.sep.join([data_dir, filename])
                if not os.path.exists(source_path):
                    # The file has been deleted, remove it from the backup
                    print 'Removing file', backup_path
                    os.remove(backup_path)

    # Log all files skipped due to size or other restrictions
    if skipped_files:
        with open('skipped.log', 'w') as f:
            f.writelines(skipped_files)
    print


if __name__ == '__main__':
    # Replace this with your backup and data location
    BACKUP_DIR = os.path.expanduser('~/Dropbox/backup')
    DATA_DIR = os.path.expanduser('~/Desktop')

    # Maximum size of file to be backed up (in bytes)
    MAX_FILE_SIZE = 25 * 1024 * 1024

    backup_files(DATA_DIR, BACKUP_DIR, MAX_FILE_SIZE)
