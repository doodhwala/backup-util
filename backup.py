import os
import shutil

# Replace this with your backup and data location
BACKUP_DIR = os.path.expanduser('~/Dropbox/backup')
DATA_DIR = os.path.expanduser('~/Desktop')

# Maximum size of file to be backed up (in bytes)
MAX_FILE_SIZE = 25 * 1024 * 1024


def get_backup_path(data_path):
    return data_path.replace(DATA_DIR, BACKUP_DIR)


if __name__ == '__main__':
    # By default, this ignores hidden files and directories (beginning with .)

    skipped_files = []
    for (dirpath, dirnames, filenames) in os.walk(DATA_DIR):
        # If the current folder is hidden, ignore it
        if '.' in dirpath:
            pass
        else:
            backup_path = get_backup_path(dirpath)
            if not os.path.exists(backup_path):
                os.mkdir(backup_path)
            for filename in filenames:
                source_path = os.sep.join([dirpath, filename])
                dest_path = os.sep.join([backup_path, filename])
                if os.path.getsize(source_path) <= MAX_FILE_SIZE:
                    if os.path.exists(dest_path):
                        # If a new version of the file is present, overwrite the old backup
                        if os.path.getmtime(source_path) > os.path.getmtime(dest_path):
                            print 'Updating backup of', source_path
                            shutil.copyfile(source_path, dest_path)
                    else:
                        # If the file does not exist, create a backup
                        print 'Creating backup of', source_path
                        shutil.copyfile(source_path, dest_path)
                else:
                    skipped_files.append(source_path + '\n')
                    print 'File is too big - skipping', source_path

    if skipped_files:
        with open('skipped.log', 'w') as f:
            f.writelines(skipped_files)
