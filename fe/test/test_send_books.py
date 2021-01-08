import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.new_seller import register_new_seller
from fe.access import buyer,auth
from fe import conf
import uuid


class TestSendBooks:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_send_books_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_send_books_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_send_books_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        # self.seller = register_new_seller(self.seller_id, self.seller_id)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        self.seller = self.gen_book.get_seller()
        yield

    # def test_non_exist_order_id(self):
    #

    def test_send_books_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code0, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.seller.send_books(self.store_id,order_id)
        assert code == 200

    def test_non_exist_book_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=True, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code != 200


    def test_non_exist_order_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code0, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.seller.send_books(self.store_id, order_id+ "_x")
        assert code != 200


    def test_non_exist_store_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.seller.send_books(self.store_id+ "_x", order_id)
        assert code != 200

    def test_receive_books_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.seller.send_books(self.store_id,order_id)
        code = self.buyer.receive_books(self.buyer_id, self.password, order_id)
        assert code == 200

    def test_receive_non_exist_buyer_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.seller.send_books(self.store_id,order_id)
        code = self.buyer.receive_books(self.buyer_id+ "_x", self.password, order_id)
        assert code != 200


    def test_receive_non_exist_order_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.seller.send_books(self.store_id,order_id)
        code = self.buyer.receive_books(self.buyer_id, self.password, order_id+ "_x")
        assert code != 200

    def test_cancel_order_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.buyer.cancel(self.buyer_id,order_id)
        assert code == 200

    def test_cancel_non_exist_buyer_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.buyer.cancel(self.buyer_id+ "_x",order_id)
        assert code != 200

    def test_cancel_non_exist_order_id(self):
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        code = self.buyer.cancel(self.buyer_id,order_id+ "_x")
        assert code != 200

    def test_search_ok(self):#分页
        code, result = self.buyer.search("三毛", 0)
        assert code == 200

    def test_search_ok_page(self):#全部显示
        code, result = self.buyer.search("三毛", 1)
        assert code == 200

    def test_search_empty_content(self):
        code, result = self.buyer.search("三毛+", 1)
        assert result==[]

    def test_search_empty_page(self):
        code, result = self.buyer.search("三毛", 1000)
        assert result==[]

    def test_search_empty(self):
        code, result = self.buyer.search("三毛+", 1000)
        assert result==[]

    def test_search_many_ok(self):
        list=["三毛","袁氏"]
        code, result = self.buyer.search_many(list)
        assert code == 200

    def test_search_many_u_ok(self):  # 分页
        list = ["三毛", "袁氏", "心灵"]
        code, result = self.buyer.search_many(list)
        assert code == 200

    def test_search_many_ok_u(self):
        list=["三毛","袁氏++"]
        code, result = self.buyer.search_many(list)
        assert code == 200

    def test_search_many_empty(self):#分页
        list=["三毛+","袁氏++"]
        code, result = self.buyer.search_many(list)
        assert result==[]




    # def test_receive_pwd_error(self):#receive book未检查密码
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    #     assert ok
    #     code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     code = self.seller.send_books(self.store_id,order_id)
    #     code = self.buyer.receive_books(self.buyer_id, self.password+ "_x", order_id)
    #     assert code != 200




    # def test_non_exist_book_id(self):
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=True, low_stock_level=False)
    #     assert ok
    #     code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     assert code != 200
    #
    # def test_low_stock_level(self):
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=True)
    #     assert ok
    #     code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     assert code != 200
    #
    # def test_ok(self):
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    #     assert ok
    #     code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     assert code == 200
    #
    # def test_non_exist_user_id(self):
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    #     assert ok
    #     self.buyer.user_id = self.buyer.user_id + "_x"
    #     code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
    #     assert code != 200
    #
    # def test_non_exist_store_id(self):
    #     ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    #     assert ok
    #     code, _ = self.buyer.new_order(self.store_id + "_x", buy_book_id_list)
    #     assert code != 200
