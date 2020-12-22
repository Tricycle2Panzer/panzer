from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging
import datetime

# 配置定时任务
class Config(object):
    JOBS = [
        {
            'id': 'soft_real_time',
            'func': '__main__:time_exceed_cancel',
            'trigger': 'interval',
            'seconds': 3600,
        }
    ]