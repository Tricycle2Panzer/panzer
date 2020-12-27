import datetime
from be.model.timer import get_time_stamp
from be.model.timer import get_time_now
daemon = 0
to_be_paid = [[daemon,get_time_stamp()]]
# to_be_paid.append([daemon2,get_time_stamp()])
# print(int(to_be_paid[0][1]))
# print(to_be_paid[1][1])

def add_order(orderID):
    to_be_paid.append([orderID,int(get_time_stamp())])
    return 1

def delete_pending_order(orderID):
    for i in range(0,len(to_be_paid)):
        if to_be_paid[i][0]==orderID:
            to_be_paid.pop(i) #will return something
            break
    return 0