from be.model import db_conn

class sqls(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def can_sql(self,orderID):
        self.conn.execute(
            "UPDATE new_order set status=0 where order_id = '%s' ;" % (orderID))

        self.conn.commit()
        print("cansql")
        return

