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
    trigger=IntervalTrigger(seconds=2),
    id='printing_time_job',
    name='Print time every 2 seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

from app import routes

# run Flask app in debug mode
app.run(debug=True)
