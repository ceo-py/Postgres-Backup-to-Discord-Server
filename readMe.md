# PostgreSQL Backup to Discord Server

Automate the backup process of PostgreSQL databases and securely store them on your Discord server with this Python script. The script ensures that your valuable data is regularly backed up and readily accessible whenever needed.

## Features

- **Automated Backups**: Schedule daily backups of PostgreSQL databases without manual intervention.
- **Change Detection**: Compare current and previous backups to detect any changes in your database, ensuring data integrity.
- **Discord Integration**: Seamlessly send backup files to your Discord server using a webhook for easy access and management.
- **File Renaming**: Organize backup files by renaming them for better organization and easier identification.

## Requirements

Ensure the following prerequisites are met before running the script:

- Python 3.x installed on your system.
- PostgreSQL installed and accessible on your server.
- Discord server with webhook integration enabled.

## Configuration

Before running the script, configure the following variables to match your PostgreSQL setup and Discord server:

```python
import hashlib
import requests
import subprocess
import datetime
import os

# Specify PostgreSQL database connection details
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "username"
DB_PASSWORD = "user password"

# Discord webhook URL for sending backup files
WEBHOOK_URL = 'Discord Webhook link'

# List of database names to be backed up
db_base_names = []

# Set the PostgreSQL password as an environment variable
os.environ['PGPASSWORD'] = DB_PASSWORD
```

## Automated Backup Setup

Set up automated daily backups by following these steps:

Install as a Linux Service: Start the backup automation service by copying the provided service and timer files to /etc/systemd/system and running the following commands:
```terminal
systemctl daemon-reload
sudo systemctl start db-backup.service
sudo systemctl enable db-backup.timer
sudo systemctl start db-backup.timer
```

Schedule Backups: The service is configured to run daily at 23:00, ensuring your databases are backed up regularly without manual intervention.
