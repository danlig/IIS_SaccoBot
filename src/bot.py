from apscheduler.schedulers.blocking import BlockingScheduler
from telegram.ext import Updater
from news import check_updates
import os

def main():
    """Avvia IIS Sacco Bot."""
    # LOG: START
    print("[START] Inizializzando bot...")

    # Inizializza bot
    token = os.environ['TOKEN']
    bot = Updater(token).bot

    # Inizializza scheduler
    sched = BlockingScheduler()
    # Imposta interval job
    sched.add_job(check_updates, 'interval', minutes=10,
                    args=[bot])
    # Avvia scheduler
    sched.start()

    # LOG: STARTED
    print("[STARTED] Bot avviato correttamente")

if __name__ == '__main__':
    main()