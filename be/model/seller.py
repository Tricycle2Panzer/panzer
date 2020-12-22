from be.model import error
from be.model import db_conn
import sqlalchemy
import json
from pymongo.errors import PyMongoError
from be.model import nlp


class Seller(db_conn.DBConn):

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            book_info_json = json.loads(book_json_str)

            # ---分离作者国籍开始---
            # 将作者栏中的作者国籍拆出，便于建立倒排表

            # ---分离作者国籍结束---

            # ---提取关键字开始---
            # 提取简介及目录中关键字，并将关键字加入书的标签
            tags = []
            if "tags" in book_info_json.keys():
                tags = book_info_json.get("tags")
            if "author_intro" in book_info_json.keys():
                keyword = nlp.get_keyword(book_info_json.get("author_intro"))
                tags += keyword
            if "book_intro" in book_info_json.keys():
                keyword = nlp.get_keyword(book_info_json.get("book_intro"))
                tags += keyword
            if "content" in book_info_json.keys():
                keyword = nlp.get_keyword(book_info_json.get("content"))
                tags += keyword
            book_info_json["tags"] = tags
            # ---提取关键字结束---

            # ---加入倒排索引开始---
            # 将新书的标题、作者、标签加入倒排索引表

            # ---加入倒排索引结束---

            price = book_info_json.get("price")
            book_info_json.pop("price")
            response = self.mongo['book'].insert_one(book_info_json)
            mongo_id = str(response.inserted_id)
            # print(response.inserted_id)
            # self.conn.execute("INSERT into store(store_id, book_id, book_info, stock_level) VALUES (:sid, :bid, :bif, :skl)",
            #                   {'sid':store_id, 'bid':book_id, 'bif':book_json_str, 'skl':stock_level})
            self.conn.execute(
                "INSERT into store(store_id, book_id, stock_level, price) VALUES (:sid, :bid, :skl, :prc)",
                {'sid': store_id, 'bid': book_id, 'skl': stock_level, 'prc': price})
            self.conn.commit()
        except PyMongoError as e:
            return 529, "{}".format(str(e))
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            self.conn.execute("UPDATE store SET stock_level = stock_level + :asl  WHERE store_id = :sid AND book_id = :bid",
                              {'asl':add_stock_level, 'sid':store_id, 'bid':book_id})
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)
            self.conn.execute("INSERT into user_store(store_id, user_id) VALUES (:sid, :uid)", {'sid':store_id, 'uid':user_id})
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    # 卖家发货
    def send_books(self,seller_id,order_id):
        try:
            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)
            # if not self.order_id_exist(order_id):  #增加order_id不存在的错误处理
            #     return error.error_non_exist_order_id(order_id)

            self.conn.execute(
                "UPDATE new_order set status=2 where order_id = '%s' ;" % (order_id))
            self.conn.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
