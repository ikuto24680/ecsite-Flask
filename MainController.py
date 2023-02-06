from flask import Flask, render_template, redirect, request, url_for, session
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.sql import select, insert
from MainModel import users, items, toppings, orders, order_items, order_toppings

ecsite = Flask(__name__)

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/student")

conn = engine.connect()

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
            if password == user.password:
                return redirect("/list")
            else:
                return render_template("login.html", loginError='メールアドレスまたはパスワードが間違っています。')
        except:
            return render_template("login.html", loginError='メールアドレスまたはパスワードが間違っています。')
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

    with open('documents/item_detail_findAll_toppings.txt', 'r') as txt:
        toppingselect = text(txt.readline())
        toppingList = conn.execute(toppingselect)
    return render_template("item_detail.html", item=item, toppingList=toppingList)


@ecsite.route("/cart")
def cart():
    conn.rollback()

    if request.method == "POST":
        order = session.get['user']
        itemId = request.form['itemId']
        size = request.form['size']
        toppingList = request.form['toppingList']
        quantity = request.form['quantity']
        iteminsert = insert(items)
        inserteditems = select(items)
    # ユーザーを指定してカートを表示
