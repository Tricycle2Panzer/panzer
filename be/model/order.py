from be.model import db_conn
from sqlalchemy.exc import IntegrityError

class Order(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def cancel_order(self,orderID):
        try:
            self.conn.execute(
                "UPDATE new_order set status=0 where order_id = '%s' ;" % (orderID))
            self.conn.commit()
            print("cansql")
        except IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

