import requests
import hashlib
import subprocess
import datetime
import os

# put db names inside
db_base_names = ["****"]

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "****"
DB_PASSWORD = "****"
WEBHOOK_URL = 'discord web hook address'
OUTPUT_ZIP = "file_name.zip"

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


def checksum_files(backup_file: str, old_backup_file: str) -> bool:
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
    requests.post(webhook_url, data=data)
    create_zip(file_path, webhook_url, OUTPUT_ZIP)


def create_zip(file_name, webhook_url, output_zip):
    command = [
        'zip', output_zip, file_name
    ]

    subprocess.run(command, check=True)
    send_file(output_zip, webhook_url)


def send_file(file_path, webhook_url):
    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file)}
        response = requests.post(webhook_url, files=files)

        if response.status_code == 200:
            os.remove(file_path)


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