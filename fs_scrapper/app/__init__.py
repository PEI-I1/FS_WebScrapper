from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import time
from app import updater

app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=updater.updater,
    trigger=IntervalTrigger(hours=24),#ALTERAR AQUI PARA MUDAR O TEMPO EM QUE FAZ UPDATE
    id='printing_time_job',
    name='Print time every 24 hours',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

scheduler2 = BackgroundScheduler()
scheduler2.start()
scheduler2.add_job(
    func=updater.updater2,
    trigger=IntervalTrigger(hours=168),#ALTERAR AQUI PARA MUDAR O TEMPO EM QUE FAZ UPDATE
    id='printing_time_job',
    name='Print time every 168 hours',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler2.shutdown())

# run Flask app in debug mode
app.run(debug=True, host='0.0.0.0')
from app import routes
