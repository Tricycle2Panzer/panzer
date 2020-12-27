import datetime
import time

def get_time_now(): #day h min and sec
    cur_time=datetime.datetime.now()
    return cur_time

def get_time_stamp(): #get timestamp for auto cancelling orders that are not paid in time
    cur_time_stamp = time.time()
    return cur_time_stamp

# timestamp = get_time_stamp()
# print(timestamp)