from be.model.timer import get_time_stamp
from be.model.sqlsys import sqls
time_limit=30 # 订单存活时间
daemon = 0
to_be_paid = [[daemon,get_time_stamp()]]

#优点：通过维护全局数组to_be_paid，没有额外新启线程，代价降到最低
def add_order(orderID):
    to_be_paid.append([orderID,int(get_time_stamp())])
    print("add successfully")
    print(to_be_paid)
    return 1

def delete_pending_order(orderID):
    for i in range(0,len(to_be_paid)):
        if to_be_paid[i][0]==orderID:
            to_be_paid.pop(i) #will return something
            print("AUTO DELETE ORDER")
            print(orderID)
            ss = sqls()
            ss.can_sql(orderID)
            break
    print(to_be_paid)
    return 0

def time_exceed_delete():
    del_temp=[]
    cur_time = get_time_stamp()
    for i in range(0,len(to_be_paid)):
        time_diff = cur_time-to_be_paid[i][1]
        #print(time_diff)
        if time_diff > time_limit:
            del_temp.append(to_be_paid[i][0]) #remenber, not to append the index of the array, we need the orderID
            #print('deltemp'+str(del_temp[i])) #delete the chosen item which is overdue
            #delete_pending_order(i)
    for k in range(0,len(del_temp)):
        delete_pending_order(del_temp[k])
    return 0