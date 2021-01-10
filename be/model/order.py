from be.model import db_conn
from sqlalchemy.exc import SQLAlchemyError
from be.model import error

class Order(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def cancel_order(self,order_id,end_status=0):
        try:
            cursor = self.conn.execute(
                "DELETE FROM new_order WHERE order_id = :order_id RETURNING order_id, user_id, store_id ,total_price, order_time ",
                {"order_id": order_id, })
            if cursor.rowcount == 0:
                self.conn.rollback()
                return error.error_invalid_order_id(order_id)
            row = cursor.fetchone()

            order = {
                "order_id" : row[0],
                "user_id" : row[1],
                "store_id" : row[2],
                "total_price" : row[3],  # 总价
                "order_time" : row[4],
                "status" : end_status
            }
            # self.conn.execute(
            #     "INSERT INTO old_order(order_id, store_id, user_id, total_price, status, order_time) "
            #     "VALUES(:uid, :store_id, :user_id, :total_price, :status, :order_time)",
            #     {"uid": order_id, "store_id": store_id, "user_id": buyer_id, "total_price": total_price,
            #      "status": end_status, "order_time": order_time})

            books = []
            cursor = self.conn.execute(
                "DELETE FROM new_order_detail WHERE order_id = :order_id RETURNING book_id, count, price ",
                {"order_id": order_id, })
            rows = cursor.fetchall()

            for row in rows:
                book = {
                    "book_id" : row[0],
                    "count" : row[1],
                    "price" : row[2]
                }
                if end_status == 0:
                    cursor = self.conn.execute(
                        "UPDATE store set stock_level = stock_level + :count "
                        "WHERE store_id = :store_id and book_id = :book_id ",
                        {"count": book["count"], "store_id": order["store_id"], "book_id": book["book_id"]})
                    if cursor.rowcount == 0:
                        self.conn.rollback()
                        return error.error_non_exist_book_id(book["book_id"]) + (order_id,)
                books.append(book)

                # self.conn.execute(
                #     "INSERT INTO old_order_detail(order_id, book_id, count, price) "
                #     "VALUES(:uid, :book_id, :count, :price)",
                #     {"uid": order_id, "book_id": book_id, "count": count, "price": price})
            self.commit = self.conn.commit()
            order["books"] = books
            self.mongo['history_order'].insert_one(order)
            print("cansql")
        except SQLAlchemyError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

