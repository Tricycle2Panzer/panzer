#import sqlite3 as sqlite
import uuid
import json
import logging
from be.model import db_conn
from be.model import error
import sqlalchemy


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    # #判断user是否存在
    # def check_user(self, user_id):
    #     user = self.conn.execute("SELECT user_id FROM user WHERE user_id = '%s';" % (user_id,)).fetchone()
    #     if user is None:
    #         return False
    #     else:
    #         return True
    #
    # #判断store是否存在
    # def check_store(self, store_id):
    #     store = self.conn.execute("SELECT store_id FROM user_store WHERE store_id = '%s';" % (store_id,)).fetchone()
    #     if store is None:
    #         return False
    #     else:
    #         return True

    # 用户下单 买家用户ID,商铺ID,书籍购买列表(书籍购买列表,购买数量)
    def new_order(self, user_id: str, store_id: str, id_and_count: [(str, int)]) -> (int, str, str):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):#判断user存在否
                return error.error_non_exist_user_id(user_id) + (order_id, )
            if not self.store_id_exist(store_id):#判断store存在否
                return error.error_non_exist_store_id(store_id) + (order_id, )
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            total_price = 0
            for book_id, count in id_and_count:
                cursor = self.conn.execute(
                    "SELECT book_id, stock_level, price FROM store "
                    "WHERE store_id = :store_id AND book_id = :book_id",
                    {"store_id":store_id, "book_id":book_id})
                row = cursor.fetchone()#只取最上面的第一条结果
                if row is None:
                    return error.error_non_exist_book_id(book_id) + (order_id, )

                stock_level = row[1]#库存
                #book_info = row[2] #书籍信息
                #book_info_json = json.loads(book_info)
                #price = book_info_json.get("price") #书籍价格
                price = row[2]

                if stock_level < count: #判断库存
                    return error.error_stock_level_low(book_id) + (order_id,)

                #更新库存
                cursor = self.conn.execute(
                    "UPDATE store set stock_level = stock_level - :count "
                    "WHERE store_id = :store_id and book_id = :book_id and stock_level >= :count ",
                    {"count":count, "store_id":store_id, "book_id":book_id, "count":count})
                if cursor.rowcount == 0:
                    return error.error_stock_level_low(book_id) + (order_id, )

                #创建新订单信息
                self.conn.execute(
                        "INSERT INTO new_order_detail(order_id, book_id, count, price) "
                        "VALUES(:uid, :book_id, :count, :price)",
                        {"uid":uid, "book_id":book_id, "count":count, "price":price})

                # 计算总价
                total_price += count*price

            self.conn.execute(
                "INSERT INTO new_order(order_id, store_id, user_id, total_price) "
                "VALUES(:uid, :store_id, :user_id, :total_price)",
                {"uid":uid, "store_id":store_id, "user_id":user_id, "total_price":total_price})#增加总价和订单状态
            self.conn.commit()
            order_id = uid
        except sqlalchemy.exc.IntegrityError as e:
            logging.info("528, {}".format(str(e)))
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""

        return 200, "ok", order_id

    # 买家付钱
    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        conn = self.conn
        try:
            cursor = conn.execute("SELECT order_id, user_id, store_id ,total_price FROM new_order WHERE order_id = :order_id",
                                  {"order_id": order_id, })
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row[0]
            buyer_id = row[1]
            store_id = row[2]
            total_price = row[3]# 总价

            if buyer_id != user_id:
                return error.error_authorization_fail()

            cursor = conn.execute("SELECT balance, password FROM users WHERE user_id = :buyer_id;",
                                  {"buyer_id": buyer_id, })
            row = cursor.fetchone()
            if row is None:
                return error.error_non_exist_user_id(buyer_id)
            balance = row[0]
            if password != row[1]:
                return error.error_authorization_fail()

            cursor = conn.execute("SELECT store_id, user_id FROM user_store WHERE store_id = :store_id;",
                                  {"store_id": store_id, })
            row = cursor.fetchone()
            if row is None:
                return error.error_non_exist_store_id(store_id)

            seller_id = row[1]

            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            # cursor = conn.execute("SELECT book_id, count, price FROM new_order_detail WHERE order_id = :order_id;",
            #                       {"order_id": order_id, })
            # total_price = 0
            # for row in cursor:
            #     count = row[1]
            #     price = row[2]
            #     total_price = total_price + price * count
            #
            # if balance < total_price:
            #     return error.error_not_sufficient_funds(order_id)

            # 下单扣买家的钱
            cursor = conn.execute("UPDATE users set balance = balance - :total_price1 "
                                  "WHERE user_id = :buyer_id AND balance >= :total_price2",
                                  {"total_price1": total_price, "buyer_id": buyer_id, "total_price2": total_price})
            if cursor.rowcount == 0:
                return error.error_not_sufficient_funds(order_id)

            # cursor = conn.execute("UPDATE users set balance = balance + :total_price "
            #                       "WHERE user_id = :seller_id",
            #                       {"total_price": total_price, "seller_id": seller_id})
            #
            # if cursor.rowcount == 0:
            #     return error.error_non_exist_user_id(buyer_id)

            # cursor = conn.execute("DELETE FROM new_order WHERE order_id = :order_id", {"order_id": order_id, })
            # if cursor.rowcount == 0:
            #     return error.error_invalid_order_id(order_id)
            #
            # cursor = conn.execute("DELETE FROM new_order_detail where order_id = :order_id", {"order_id": order_id, })
            # if cursor.rowcount == 0:
            #     return error.error_invalid_order_id(order_id)

            conn.commit()

        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))

        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"


    # 手动收货 改订单状态，给卖家钱
    def receive_books(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            # if not self.order_id_exist(order_id):  #增加order_id不存在的错误处理
            #     return error.error_non_exist_order_id(order_id)

            cursor = self.conn.execute("SELECT order_id, user_id, store_id ,total_price FROM new_order WHERE order_id = :order_id",
                                  {"order_id": order_id, })
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row[0]
            buyer_id = row[1]
            store_id = row[2]
            total_price = row[3]  # 总价

            if buyer_id != user_id:
                return error.error_authorization_fail()

            cursor = self.conn.execute("SELECT store_id, user_id FROM user_store WHERE store_id = :store_id;",
                                  {"store_id": store_id, })
            row = cursor.fetchone()
            if row is None:
                return error.error_non_exist_store_id(store_id)

            seller_id = row[1]

            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            cursor = self.conn.execute("UPDATE users set balance = balance + :total_price "
                                  "WHERE user_id = :seller_id",
                                  {"total_price": total_price, "seller_id": seller_id})

            if cursor.rowcount == 0:
                return error.error_non_exist_user_id(buyer_id)

            self.conn.execute(
                "UPDATE new_order set status=3 where order_id = '%s' ;" % (order_id))# 仍保留在new_order中，后续加入history后从new_order中删除
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"


    def add_funds(self, user_id, password, add_value) -> (int, str):#买家充值
        try:
            cursor = self.conn.execute("SELECT password from users where user_id=:user_id", {"user_id":user_id,})
            row = cursor.fetchone()
            if row is None:
                return error.error_authorization_fail()

            if row[0] != password:
                return error.error_authorization_fail()

            cursor = self.conn.execute(
                "UPDATE users SET balance = balance + :add_value WHERE user_id = :user_id",
                {"add_value":add_value, "user_id":user_id})
            if cursor.rowcount == 0:
                return error.error_non_exist_user_id(user_id)

            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"


    # 买家手动取消订单
    def cancel(self, buyer_id, order_id):
        try:
            if not self.user_id_exist(buyer_id):
                return error.error_non_exist_user_id(buyer_id)
            # if not self.order_id_exist(order_id):  #增加order_id不存在的错误处理
            #     return error.error_non_exist_order_id(order_id)

            self.conn.execute(
                "UPDATE new_order set status=0 where order_id = '%s' ;" % (order_id))
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def search(self, buyer_id, search_key, page):
        try:
            print(search_key)
            if not self.user_id_exist(buyer_id):
                return error.error_non_exist_user_id(buyer_id)
            page_size = 2
            page_lower = page_size * (page - 1)
            print(page_lower)

            cursor = self.conn.execute(
                "SELECT search_id, book_id from invert_index "
                "where search_key = '%s' "
                "ORDER BY search_id limit '%d' offset '%d';"
                % (search_key, page_size, page_lower))
            rows = cursor.fetchall()

            # if rows == None:  #增加searchkey不存在的错误处理
            #     return error.error_no_such_key(search_key)

            message = []
            for row in rows:
                message.append(row[1])
            print(message)

            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, message
