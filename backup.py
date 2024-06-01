import hashlib
import requests
import subprocess
import datetime
import os

# put db names inside
db_base_names = []

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "username"
DB_PASSWORD = "user password"
WEBHOOK_URL = 'Discord Webhook link'

'''
for restoring
psql -h localhost -p 5432 -U DB_USER -d DB_NAME -f BACKUP.sql
'''

os.environ['PGPASSWORD'] = DB_PASSWORD


def rename_files_in_current_directory(new_names: str) -> None:
    directory_path = os.getcwd()

    files = os.listdir(directory_path)

    for file_name in files:
        # the name of the script to skip
        if file_name == 'backup.py':
            continue

        new_name = file_name.replace('__', '_old')
        old_path = os.path.join(directory_path, file_name)
        new_path = os.path.join(directory_path, new_name)
        os.rename(old_path, new_path)


def checksum_files(backup_file: str, old_backup_file: str) -> None:
    backup_checksum = hashlib.md5(
        open(backup_file, 'rb').read()).hexdigest()
    try:
        old_backup_checksum = hashlib.md5(
            open(old_backup_file, 'rb').read()).hexdigest()
    except FileNotFoundError:
        return False

    return backup_checksum == old_backup_checksum


def send_file_to_discord_webhook(webhook_url: str, file_path: str, message: str) -> None:
    data = {
        'content': message
    }
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(webhook_url, data=data, files=files)

        if response.status_code == 200:
            print(f"Backup {message} was sent successfully to Discord.")
        else:
            print(f"Failed to send backup {message} to Discord. Status code:", response.status_code)


def check_db_for_backup() -> None:
    files_to_rename = []
    for db_name in db_base_names:
        backup_file = f'{db_name}__.sql'
        old_backup_file = f'{db_name}_old.sql'

        cmd = f'pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {db_name} > {backup_file}'
        subprocess.run(cmd, shell=True)

        if checksum_files(backup_file, old_backup_file):
            continue

        files_to_rename.append(backup_file)
        message = f'Backup of **{db_name}** changed on {datetime.datetime.now().replace(microsecond=0)}'
        send_file_to_discord_webhook(WEBHOOK_URL, backup_file, message)
    if files_to_rename:
        rename_files_in_current_directory(files_to_rename)


check_db_for_backup()
