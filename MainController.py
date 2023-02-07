from flask import Flask, render_template, redirect, request,  url_for, session, json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.sql import select, insert
import SubMethods
# from MainModel import users, items, toppings, orders, order_items, order_toppings

ecsite = Flask(__name__)

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/student")

conn = engine.connect()

ecsite.secret_key = 'user'


@ecsite.route("/", methods=['GET', 'POST'])
def login():
    conn.rollback()
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        with open('documents/register_findUserByEmail_users.txt', 'r') as txt:
            emailselect = text(txt.readline())
        try:
            connEmail = conn.execute(emailselect, {"email": email})
            for user in connEmail:
                user = user

                print("SESSIONの前")
                print(user.id)
                print(user.name)
                session["id"] = user.id
                session["name"] = user.name
                return redirect("/list")
            else:
                return render_template("login.html", loginError='メールアドレスまたはパスワードが間違っています。')
        except:
            return render_template("login.html", loginError='メールアドレスまたはパスワードが間違っていますよん。')
    if request.method == 'GET':
        return render_template("login.html")

    return render_template("login.html")


@ecsite.route("/register", methods=['GET', 'POST'])
def register():
    conn.rollback()
    if request.method == "POST":
        lastName = request.form['lastName']
        firstName = request.form['firstName']
        name = lastName + firstName
        email = request.form['email']
        zipcode = request.form['zipcode']
        address = request.form['address']
        telephone = request.form['telephone']
        password = request.form['password']
        confimationPassword = request.form['confimationPassword']
        blank = ''

        if lastName is blank or firstName is blank or email is blank or zipcode is blank or address is blank or telephone is blank or password is blank or confimationPassword is blank:
            return render_template("register_user.html", registerError='全項目必須です。')

        with open('documents/register_findUserByEmail_users.txt', 'r') as txt:
            emailselect = text(txt.readline())
            userList = []
        try:
            emailList = conn.execute(emailselect, {"email": email})
            for user in emailList:
                userList.append(user)
            if len(userList) != 0:
                return render_template("register_user.html", registerError='既に登録済みのメールアドレスです。')
        except:
            emailList = 0

        if not password == confimationPassword:
            return render_template("register_user.html", registerError='確認用パスワードが一致しません。')

        print("insert直前")
        with open('documents/register_insertUser_users.txt', 'r') as txt:
            userinsert = text(txt.readline())
            conn.execute(userinsert, {"name": name, "email": email, "password": password,
                                      "zipcode": zipcode, "address": address, "telephone": telephone})
            conn.commit()
        return render_template("login.html")

    return render_template("register_user.html")


@ecsite.route("/list", methods=['GET', 'POST'])
def item_list():
    conn.rollback()
    if request.method == "GET":
        # itemselect = select(items)
        with open('documents/item_list_findAll_items.txt', 'r') as txt:
            itemselect = text(txt.readline())
            itemList = conn.execute(itemselect)
    else:
        search = request.form['name']
        search = '%'+search+'%'
        # itemselect = select(items).where(
        #     items.name.like('%{}%').format(search))
        with open('documents/item_list_findByName_items.txt', 'r') as txt:
            itemselect = text(txt.readline())
            itemList = conn.execute((itemselect), {"name": search})

    return render_template('item_list.html', itemList=itemList)


@ecsite.route("/detail/<int:itemId>")
# @ecsite.route("/detail")
def item_detail(itemId):
    conn.rollback()

    itemId = str(itemId)
    with open('documents/item_detail_findByItemId_items.txt', 'r') as txt:
        itemselect = text(txt.readline())
        itemList = conn.execute(itemselect, {"itemId": itemId})
        for item in itemList:
            item = item
            print(item)
            print(type(item))

    with open('documents/item_detail_findAll_toppings.txt', 'r') as txt:
        toppingselect = text(txt.readline())
        toppingList = conn.execute(toppingselect)
    return render_template("item_detail.html", item=item, toppingList=toppingList)


@ecsite.route("/cart", methods=['GET', 'POST'])
def cart():
    conn.rollback()

    if 'id' in session:

        id = session['id']
        if request.method == "POST":
            # order = session.get['user']
            itemId = request.form['itemId']
            size = request.form['size']
            toppingList = request.form['toppingList']
            print("toppingList".format(toppingList))
            quantity = request.form['quantity']
            subtotal = SubMethods.subtotal(itemId, size, toppingList, quantity)
            print("subtotal={}".format(subtotal))

            # ここの段階までにsubtotalを出しておく。

        # そのユーザーに注文前のOrderが存在するかどうか
        with open('documents/cart_findOrderByUserId_orders.txt', 'r') as txt:
            orderselect = text(txt.readline())
            connOrder = conn.execute(orderselect, {"id": id}).one_or_none()
            # None（注文前のOrderが存在していない時）→新しく作る。
            if connOrder is None:
                # orderinsert = insert(orders)
                with open('documents/cart_insertOrder_orders.txt', 'r') as txt:
                    orderinsert = text(txt.readline())
                    connOrder = conn.execute(orderinsert, {"userId": id})
                conn.commit()
                conn.rollback()
        # 上で作ったOrdersをSELECTする
        with open('documents/cart_findOrderByUserId_orders.txt', 'r') as txt:
            orderselect = text(txt.readline())
            connOrderPlus = conn.execute(orderselect, {"id": id})
        conn.rollback()

        print("connOrderPlusの中身")
        print(connOrderPlus)
        # この時点ではログイン中ユーザーのOrdersが存在している前提
        # 1つの注文前Orderをfor文で取り出す
        for order in connOrderPlus:
            # orderId = order.id
            # OrderIdを基にOrderItemsをInsert
            with open('documents/cart_insertOrderItem_order_items.txt', 'r') as txt:
                orderItemInsert = text(txt.readline())
                print("order.id={}".format(order.id))
                connOrderItem = conn.execute(orderItemInsert, {
                    "item_id": itemId, "order_id": order.id, "quantity": quantity, "size": size, "subtotal": subtotal})
                conn.commit()
            # OrderItemIdを基にOrderToppingをInsert
            with open('documents/cart_findOrderItemById_orderItems.txt', 'r') as txt:
                orderItemselect = text(txt.readline())
                connOrderItem = conn.execute(orderItemselect)
                conn.rollback()
                for orderItem in connOrderItem:
                    # print("orderItemの中身")
                    # print(orderItem)
                    orderItemId = orderItem[0]
                    # print(orderItemId)
                    for topping in toppingList:
                        with open('documents/cart_insertOrderTopping_order_toppings.txt', 'r') as txt:
                            insertOrderTopping = text(txt.readline())
                            connOrderTopping = conn.execute(
                                insertOrderTopping, {"toppingId": topping, "orderItemId": orderItemId})
                conn.commit()
        # 以下3つのSELECT文をResultSet的なテーブル結合で一度に取り出す。
        with open('documents/cart_findOrderByUserId_orders.txt', 'r') as txt:
            orderselect = text(txt.readline())
            Cart = conn.execute(orderselect, {"id": id})

            for order in Cart:
                with open('documents/cart_findByOrderId_orderItems.txt', 'r') as txt:
                    orderItemselect = text(txt.readline())
                    itemInCart = conn.execute(
                        orderItemselect, {"orderid", order.id})

                    for item in itemInCart:
                        with open('documents/cart_findByOrderItemId_orderToppings.txt', 'r') as txt:
                            orderToppingselect = text(txt.readline())
                            toppingInCart = conn.execute(
                                orderToppingselect, {"orderItemId", item.id})

        return render_template('cart_list.html', Cart=Cart, itemInCart=itemInCart, toppingInCart=toppingInCart)
    else:
        return redirect("/")


def login_check():
    if 'id' in session:
        return True
    else:
        return False


def subtotal(itemId, size, toppingList, quantity):
    subtotal = 0
    if size == 'M':
        with open('documents/subtotal_findById_items.txt', 'r') as txt:
            itemselect = text(txt.readline())
            connItem = conn.execute(itemselect, {"itemId": itemId})
            for item in connItem:
                for topping in toppingList:
                    with open('documents/subtotal_findById_toppings.txt', 'r') as txt:
                        toppingselect = text(txt.readline())
                        connTopping = conn.execute(
                            toppingselect, {"toppingId": topping})
                        subtotal += connTopping.price_m
                subtotal += item.price_m
            subtotal = subtotal * quantity
    else:
        with open('documents/subtotal_findById_items.txt', 'r') as txt:
            itemselect = text(txt.readline())
            connItem = conn.execute(itemselect, {"itemId": itemId})
            for item in connItem:
                for topping in toppingList:
                    with open('documents/subtotal_findById_toppings.txt', 'r') as txt:
                        toppingselect = text(txt.readline())
                        connTopping = conn.execute(
                            toppingselect, {"toppingId": topping})
                        subtotal += connTopping.price_l
                subtotal += item.price_l
            subtotal = subtotal * quantity
            print(subtotal)
    return subtotal
