from flask import Blueprint
from flask import request
from flask import jsonify
from be.model.buyer import Buyer

bp_buyer = Blueprint("buyer", __name__, url_prefix="/buyer")


@bp_buyer.route("/new_order", methods=["POST"])
def new_order():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    books: [] = request.json.get("books")
    id_and_count = []
    for book in books:
        book_id = book.get("id")
        count = book.get("count")
        id_and_count.append((book_id, count))

    b = Buyer()
    code, message, order_id = b.new_order(user_id, store_id, id_and_count)
    return jsonify({"message": message, "order_id": order_id}), code


@bp_buyer.route("/payment", methods=["POST"])
def payment():
    user_id: str = request.json.get("user_id")
    order_id: str = request.json.get("order_id")
    password: str = request.json.get("password")
    b = Buyer()
    code, message = b.payment(user_id, password, order_id)
    return jsonify({"message": message}), code


@bp_buyer.route("/add_funds", methods=["POST"])
def add_funds():
    user_id = request.json.get("user_id")
    password = request.json.get("password")
    add_value = request.json.get("add_value")
    b = Buyer()
    code, message = b.add_funds(user_id, password, add_value)
    return jsonify({"message": message}), code

# 收货
@bp_buyer.route("/receive_books", methods=["POST"])
def send_books():
    user_id: str = request.json.get("user_id")
    order_id: str = request.json.get("order_id")
    password: str = request.json.get("password")
    b = Buyer()
    code, message = b.receive_books(user_id, password, order_id)

    return jsonify({"message": message}), code


# 手动取消订单
@bp_buyer.route("/cancel_order", methods=["POST"])
def cancel():
    user_id: str = request.json.get("buyer_id")
    order_id: str = request.json.get("order_id")
    b = Buyer()
    code, message = b.cancel(user_id,order_id)
    return jsonify({"message": message}), code

@bp_buyer.route("/search", methods=["POST"])
def search():
    user_id: str = request.json.get("buyer_id")
    search_key: str = request.json.get("search_key")
    page: str = request.json.get("page")
    b = Buyer()
    code, message = b.search(user_id, search_key, page)
    return jsonify({"message": message}), code