from flask import Flask, render_template, redirect, request,  url_for, session, json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.sql import select, insert
from MainModel import users, items, toppings, orders, order_items, order_toppings
import SubController
import cgi
from datetime import datetime, date


ecsite = Flask(__name__)

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/student")

conn = engine.connect()

ecsite.secret_key = 'user'

listForm = cgi.FieldStorage()

blank = ''

orderBlank = False


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

    with open('documents/item_detail_findAll_toppings.txt', 'r') as txt:
        toppingselect = text(txt.readline())
        toppingList = conn.execute(toppingselect)
    return render_template("item_detail.html", item=item, toppingList=toppingList)


@ecsite.route("/cart", methods=['GET', 'POST'])
def cart():
    print("cartにもきてる")
    conn.rollback()

    if 'id' in session:

        id = session['id']
        if request.method == "POST":
            # order = session.get['user']
            itemId = request.form['itemId']
            size = request.form['size']
            toppingList = request.form['toppingList']
            quantity = request.form['quantity']
            subtotal = SubController.subtotal(
                itemId, size, toppingList, quantity)

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

            # この時点ではログイン中ユーザーのOrdersが存在している前提
            # 1つの注文前Orderをfor文で取り出す
            for order in connOrderPlus:
                # orderId = order.id
                # OrderIdを基にOrderItemsをInsert
                with open('documents/cart_insertOrderItem_order_items.txt', 'r') as txt:
                    orderItemInsert = text(txt.readline())
                    connOrderItem = conn.execute(orderItemInsert, {
                        "item_id": itemId, "order_id": order.id, "quantity": quantity, "size": size, "subtotal": subtotal})
                    conn.commit()
                # OrderItemIdを基にOrderToppingをInsert
                with open('documents/cart_findOrderItemById_orderItems.txt', 'r') as txt:
                    orderItemselect = text(txt.readline())
                    connOrderItem = conn.execute(orderItemselect)
                    conn.rollback()
                    for orderItem in connOrderItem:
                        orderItemId = orderItem[0]
                        for topping in toppingList:
                            with open('documents/cart_insertOrderTopping_order_toppings.txt', 'r') as txt:
                                insertOrderTopping = text(txt.readline())
                                connOrderTopping = conn.execute(
                                    insertOrderTopping, {"toppingId": topping, "orderItemId": orderItemId})
                    conn.commit()

        # OrderIdをもとにOrderItemのリスト、OrderItemIdをもとにOrderToppingのロストを取得
        # OrderItemのリストの数だけOrderToppingのリストも数があるから、Modelにセットしなくても行ける？
        #     with open('documents/cart_findByOrderId_orderItem.txt','r') as txt:
        #         orderItemselect = text(txt.readline())
        #         connOrderItem = conn.execute(orderItemselect,{"orderId":orderId})
        #         print(connOrderItem)
        #         for OrderItem in connOrderItem:
        #             OrderItemId = OrderItem.id
        #             with open('documents/cart_findByOrderItemId_orderToppings.txt','r') as txt:

        # そもそも、元のResultSetのSQL文から持って凝ればいいんじゃないか説
        HTMLOrderList = list()
        tax = 0
        totalprice = 0
        subtotal = 0
        with open('documents/cart_findOrderIdByUserId_orders.txt', 'r') as txt:
            orderselect = text(txt.readline())
            connOrderPlus = conn.execute(orderselect, {"id": id}).one_or_none()
        conn.rollback()
        print("connOrderPlusのtypeは")
        print(type(connOrderPlus))
        for COP in connOrderPlus:
            print("COPの中身={}".format(COP))
            print(type(COP))
            orderId = COP
            with open('documents/cart_resultsetOrder_order.txt') as txt:
                orderReslutSet = text(txt.readline())
                connOrderResultSet = conn.execute(
                    orderReslutSet, {"orderId": orderId})

            for order in connOrderResultSet:
                print("order=={}".format(order))
                HTMLOrderList.append(order)
                subtotal += order.oi_subtotal

        tax = subtotal*0.1
        totalprice = int(tax + subtotal)
        orderBlankError = ''
        if orderBlank in session:
            session.pop('orderBlank', None)
            orderBlankError = 'お届け先情報を正しく記入してください'
        return render_template('cart_list.html', HTMLOrderList=HTMLOrderList, tax=tax, totalprice=totalprice, orderBlankError=orderBlankError)
    else:
        return redirect("/")


@ecsite.route("/delete", methods=['POST'])
def delete():
    orderItemId = request.form['orderItemId']
    conn.rollback()
    orderItemId = str(orderItemId)
    with open('documents/delete_deleteOrderItem_orderItems.txt', 'r')as txt:
        orderItemdelete = text(txt.readline())
        connOrderItem = conn.execute(
            orderItemdelete, {"orderItemId": orderItemId})
        conn.commit()

    return redirect("/cart")


def json_serial(obj):
    if isinstance(obj, (users)):
        return obj.isoformat()
    raise TypeError(f'Type {obj} not serializable')


def login_check():
    if 'id' in session:
        return True
    else:
        return False


@ecsite.route("/confirm")
def confirm():
    id = session['id']
    HTMLOrderList = list()
    tax = 0
    totalprice = 0
    subtotal = 0
    with open('documents/cart_findOrderIdByUserId_orders.txt', 'r') as txt:
        orderselect = text(txt.readline())
        connOrderPlus = conn.execute(orderselect, {"id": id}).one_or_none()
    conn.rollback()
    print("connOrderPlusのtypeは")
    print(type(connOrderPlus))
    for COP in connOrderPlus:
        # print("COPの中身={}".format(COP))
        # print(type(COP))
        orderId = COP
        with open('documents/cart_resultsetOrder_order.txt') as txt:
            orderReslutSet = text(txt.readline())
            connOrderResultSet = conn.execute(
                orderReslutSet, {"orderId": orderId})

        for order in connOrderResultSet:
            print("order=={}".format(order))
            HTMLOrderList.append(order)
            subtotal += order.oi_subtotal

    tax = subtotal*0.1
    totalprice = int(tax + subtotal)
    return render_template('order_confirm.html', HTMLOrderList=HTMLOrderList, tax=tax, totalprice=totalprice)


@ecsite.route("/finish", methods=['POST'])
def finish():
    id = request.form['id']
    totalprice = request.form['totalprice']
    destination_name = request.form['destinationName']
    destination_email = request.form['destinationEmail']
    destination_zipcode = request.form['destinationZipcode']
    destination_tel = request.form['destinationTel']
    try:
        delivery_date = str(datetime.strptime(
            request.form.get('deliveryDate'), '%Y-%m-%d'))
    except:
        delivery_date = ''
    # print("delivery_date=".format(delivery_date))
    # print("delivery_time=".format(delivery_time))
    delivery_time = request.form['deliveryTime']
    payment_method = request.form['paymentMethod']
    status = 1
    print("status")
    print(type(status))
    print(status)

    order_date = date.today()
    delivery_date = delivery_date[0:10]
    print(delivery_date)
    print(type(delivery_date))
    delivery_datetime = delivery_date + '-'+delivery_time
    print("delibery_datetime")
    print(type(delivery_datetime))

    print(id)
    print(totalprice)
    print(destination_name)
    print(destination_email)
    print(destination_zipcode)
    print(destination_tel)
    print(delivery_date)
    print(delivery_time)
    print(delivery_datetime)
    print(payment_method)

    if id is blank or totalprice is blank or destination_name is blank or destination_email is blank or destination_zipcode is blank or destination_tel is blank or delivery_date is blank or delivery_time is blank or payment_method is blank:
        session['orderBlank'] = True
        return redirect("/confirm")

    with open('documents/confirm_updateOrder_orders.txt')as txt:
        orderupdate = text(txt.readline())
        connOrder = conn.execute(orderupdate, {"statusA": status, "totalprice": totalprice, "order_date": order_date, "destination_name": destination_name, "destination_email": destination_email,
                                 "destination_zipcode": destination_zipcode, "destination_tel": destination_tel,  "payment_method": payment_method, "id": id})
        print("connOrder".format(connOrder))
        print(type(connOrder))
        conn.commit()

    return render_template("order_finished.html")
