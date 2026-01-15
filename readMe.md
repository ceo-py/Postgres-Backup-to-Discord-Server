# PostgreSQL Backup Script with Discord Webhook Integration

This script automates the process of backing up PostgreSQL databases, compressing backups into ZIP files, and splitting them into parts for easy handling. It also sends notifications with backup files to a Discord webhook.

## Features

* **Automated Backups**: Dumps PostgreSQL databases daily.
* **Compression**: Zips the backup files.
* **Splitting**: Splits large backups into smaller parts (max 9MB per part).
* **Discord Integration**: Sends notifications and backup files to a Discord channel via webhook.
* **File Integrity**: Verifies if a backup has changed before sending it.

## Prerequisites

* Python 3.x
* PostgreSQL
* `zip` utility installed
* A Discord webhook URL for notifications
* `pg_dump` available on the system (for database dump)

## Configuration

Before running the script, configure the following parameters:

1. **Database Configuration**:

   * `DB_HOST`: PostgreSQL server address.
   * `DB_PORT`: PostgreSQL server port (default is `5432`).
   * `DB_USER`: PostgreSQL user with access to the database.
   * `DB_PASSWORD`: Password for the PostgreSQL user.
   * `db_base_names`: List of databases to back up.

2. **Webhook URL**:

   * Set `WEBHOOK_URL` to your Discord webhook link for notifications.

3. **File Split Size**:

   * `MAX_PART_SIZE`: Maximum file size per part (default 9MB).

## How It Works

1. **Backup**: The script uses `pg_dump` to create backups of the specified databases.
2. **Checksum**: It compares the new backup with the previous one to detect changes.
3. **Zipping**: The backup is compressed into a ZIP file.
4. **Splitting**: If the backup is too large, it’s split into smaller parts (max 9MB).
5. **Sending**: Each part (or the entire zip) is uploaded to Discord via the webhook.

## Running the Script

1. **Manual Run**: Execute the script directly.

   ```bash
   python3 backup_postgress_db.py
   ```

2. **Automated Backup (via systemd)**:

   * A `systemd` service and timer are included to run the backup script daily at midnight.
   * To set up the service and timer, follow these steps:

     ```bash
     sudo systemctl enable db-backup.timer
     sudo systemctl start db-backup.timer
     ```

## Files

1. **`backup_postgress_db.py`**: Main script that handles backup, zipping, splitting, and sending to Discord.
2. **`db-backup.service`**: Systemd service for running the backup script.
3. **`db-backup.timer`**: Systemd timer to schedule the backup script.

## Restore

To restore a backup, use the following command:

```bash
psql -h localhost -p 5432 -U DB_USER -d DB_NAME -f BACKUP.sql
```


