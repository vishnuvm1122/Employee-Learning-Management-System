import os
import datetime
import glob
import time
from django.conf import settings
import django
import subprocess

# ---------------------------
# Django setup
# ---------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# ---------------------------
# Database config
# ---------------------------
db = settings.DATABASES['default']
backup_dir = os.path.join(os.getcwd(), "db_backups")
os.makedirs(backup_dir, exist_ok=True)

# ---------------------------
# Timestamped backup filename
# ---------------------------
date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"{db['NAME']}_{date_str}.sql.gz"
backup_path = os.path.join(backup_dir, filename)

# ---------------------------
# Build mysqldump command
# ---------------------------
# Note: password is passed in environment variable for security
env = os.environ.copy()
env['MYSQL_PWD'] = db.get('PASSWORD', '')

cmd = [
    "mysqldump",
    "-u", db["USER"],
    "-h", db.get("HOST", "localhost"),
    "-P", str(db.get("PORT", 3306)),
    db["NAME"]
]

# Run command and compress output
with open(backup_path, "wb") as f_out:
    print("Running backup:", " ".join(cmd))
    proc_dump = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)
    proc_gzip = subprocess.Popen(["gzip"], stdin=proc_dump.stdout, stdout=f_out)
    proc_dump.stdout.close()
    proc_gzip.communicate()

print(f"✅ Backup completed: {backup_path}")

# ---------------------------
# Delete backups older than 30 days
# ---------------------------
for file in glob.glob(os.path.join(backup_dir, "*.sql.gz")):
    if time.time() - os.path.getmtime(file) > 15 * 86400:
        os.remove(file)
        print(f"🗑 Deleted old backup: {file}")
