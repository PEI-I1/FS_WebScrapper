from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import time
import os
from app import updater

app = Flask(__name__)
if os.getenv('INITIAL_UPDATE', 'true') == 'true':
    updater.updater_phones_tariffs_packets_lapoio()
    updater.updater_lojas()

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=updater.updater_phones_tariffs_packets_lapoio,
    trigger=IntervalTrigger(hours=24),#ALTERAR AQUI PARA MUDAR O TEMPO EM QUE FAZ UPDATE
    id='printing_time_job',
    name='Print time every 24 hours',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

scheduler2 = BackgroundScheduler()
scheduler2.start()
scheduler2.add_job(
    func=updater.updater_lojas,
    trigger=IntervalTrigger(hours=168),#ALTERAR AQUI PARA MUDAR O TEMPO EM QUE FAZ UPDATE
    id='printing_time_job',
    name='Print time every 168 hours',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler2.shutdown())

from app import routes
