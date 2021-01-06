from be.model.order import Order
import datetime
import time

def get_time_now(): #day h min and sec
    cur_time=datetime.datetime.now()
    return cur_time

def get_time_stamp(): #get timestamp for auto cancelling orders that are not paid in time
    cur_time_stamp = time.time()
    return int(cur_time_stamp)

time_limit = 30 # 订单存活时间
unpaid_orders = {}

#优点：通过维护全局数组to_be_paid，没有额外新启线程，代价降到最低
def add_unpaid_order(orderID):
    unpaid_orders[orderID] = get_time_stamp()
    print("add successfully")
    print(unpaid_orders)
    return 200, "ok"

def delete_unpaid_order(orderID):
    try:
        unpaid_orders.pop(orderID)
        print(unpaid_orders)
    except BaseException as e:
        return 530, "{}".format(str(e))
    return 200, "ok"

def time_exceed_delete():
    del_temp=[]
    cur_time = get_time_stamp()
    o = Order()
    print("new cycle start")
    for (oid,tim) in unpaid_orders.items():
        time_diff = cur_time - tim
        if time_diff > time_limit:
            del_temp.append(oid)  # remenber, not to append the index of the array, we need the orderID
    for oid in del_temp:
        delete_unpaid_order(oid)
        o.cancel_order(oid)
    return 0