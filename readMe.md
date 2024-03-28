# PostgreSQL Backup to Discord Server

This Python script performs automated backups of PostgreSQL databases and sends them to a Discord server for storage.

## Features

- Automatically backup PostgreSQL databases.
- Compare current and previous backups to detect changes.
- Send backup files to a Discord server using a webhook.
- Rename backup files for better organization.

## Requirements

- Python 3.x
- `requests` library (install with `pip install requests`)
- PostgreSQL installed and accessible
- Discord server with webhook integration

## Configuration

Before running the script, make sure to configure the following variables in the script:

```python
import hashlib
import requests
import subprocess
import datetime
import os

# Put db names inside
db_base_names = []

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "username"
DB_PASSWORD = "user password"
WEBHOOK_URL = 'Discord Webhook link'

os.environ['PGPASSWORD'] = DB_PASSWORD
