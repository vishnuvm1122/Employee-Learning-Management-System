import os
import logging
import subprocess
import threading
from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils import timezone as dj_timezone

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Prevent duplicate scheduler in multiple reloads
        if os.environ.get("RUN_MAIN") != "true":
            return

        try:
            scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

            scheduler.add_job(
                self.run_backup_script,
                CronTrigger(hour=22, minute=0)  # 10:00 PM IST
            )

            scheduler.start()
            logger.info("✅ APScheduler started (daily at 10:00 PM IST)")

        except Exception as e:
            logger.exception(f"Scheduler failed to start: {e}")

    def run_backup_script(self):
        logger = logging.getLogger(__name__)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(base_dir, "backup-db.py")

        python_path = os.path.join(base_dir, "venv", "bin", "python")

        try:
            subprocess.run(
                [python_path, script_path],
                check=True
            )
            logger.info("✅ Backup script executed successfully")

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Backup script failed: {e}")

        except Exception as e:
            logger.exception(f"⚠️ Unexpected error: {e}")