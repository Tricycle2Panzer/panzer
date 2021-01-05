from be import serve
from flask import Blueprint
from flask import Flask, render_template
import os
import sys
from be.model.order import time_exceed_delete
from flask import Flask
from flask_apscheduler import APScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
#app = Flask(__name__)

if __name__ == "__main__":
    serve.be_run(auto_timer=True)

