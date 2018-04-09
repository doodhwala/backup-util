# backup-util
Backup utility to periodically create local copies of data

_You don't know what you have until it's gone_

Features to be supported:
- Inclusion and exclusion list
    - Whitelist folders
    - Blacklist files, folders and extensions
- Filter by file size
    - Items above a max file size should give a prompt
- Automatic / scheduled
    - Run either daily, hourly or based on user specified frequency
- Hacky Dropbox integration
    - Does not use the Dropbox API
    - Set your backup destination as the Dropbox folder
    - Let Dropbox's daemon take care of the syncing