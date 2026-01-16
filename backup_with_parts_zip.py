import requests
import hashlib
import subprocess
import datetime
import os

# put db names inside
db_base_names = ["names of each db you want to back up"]

DB_HOST = "HOST"
DB_PORT = "PORT"
DB_USER = "USERNAME"
DB_PASSWORD = "PASSWORD"
WEBHOOK_URL = "WEBHOOK URL"
OUTPUT_ZIP = "NAME OF THE ZIP FILE"
MAX_PART_SIZE = "9m"  # 9MB in bytes

'''
Backup Restore:
  psql -h localhost -p 5432 -U DB_USER -d DB_NAME -f BACKUP.sql

File Zipping:
  zip -s 9m new.zip <file_name>

File Merging (Unix):
  cat new.z*[0-9]* new.zip > existing.zip
'''

os.environ['PGPASSWORD'] = DB_PASSWORD


def rename_files_in_current_directory(new_names: str) -> None:
    directory_path = os.getcwd()
    files = os.listdir(directory_path)

    for file_name in files:
        # the name of the script to skip
        if ".py" in file_name:
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


def send_initial_discord_mesage(webhook_url: str, message: str) -> None:
    data = {
        'content': message
    }
    requests.post(webhook_url, data=data)


def zip_file(file_name, output_zip):
    """Zip the original file into a single zip archive."""
    command = ['zip', '-s', MAX_PART_SIZE, output_zip, file_name]
    subprocess.run(command, check=True)
    print(f"Zip file {output_zip} created successfully.")


def send_file(file_path, webhook_url):
    """Send the file to the Discord webhook."""
    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file)}
        response = requests.post(webhook_url, files=files)

        if response.status_code == 200:
            print(f"File {file_path} sent successfully!")
            os.remove(file_path)  # Delete the file only if it was successfully sent
        else:
            print(f"Failed to send {file_path}. Status code: {response.status_code}")


def create_zip_and_split(file_name, webhook_url, output_zip_prefix):
    """Create a zip of the file, split it into parts, and send each part to Discord."""
    output_zip = f"{output_zip_prefix}.zip"
    zip_file(file_name, output_zip)

    directory_path = os.getcwd()
    files = os.listdir(directory_path)

    for file_name in files:
        if ".z" not in file_name:
            continue

        send_file(file_name, webhook_url)


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
        send_initial_discord_mesage(WEBHOOK_URL, message)
        create_zip_and_split(backup_file, WEBHOOK_URL, db_name)
    if files_to_rename:
        rename_files_in_current_directory(files_to_rename)


check_db_for_backup()