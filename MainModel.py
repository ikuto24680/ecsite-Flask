# from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey,  VARCHAR

# metadata_obj = MetaData()

# users = Table(
#     "users",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(100), nullable=False),
#     Column("email", String(100), nullable=False, unique=True),
#     Column("password", String, nullable=False),
#     Column("zipcode", String(8), nullable=False),
#     Column("address", String(200), nullable=False),
#     Column("telephone", String(15), nullable=False),
# )

# items = Table(
#     "items",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("description", String, nullable=False),
#     Column("price_m", Integer, nullable=False),
#     Column("price_l", Integer, nullable=False),
#     Column("image_path", String, nullable=False),
#     # Column("deleted", boolean, default='false', nullable=True),
# )

# toppings = Table(
#     "toppings",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("price_m", Integer, nullable=False),
#     Column("price_l", Integer, nullable=False),
# )

# orders = Table(
#     "orders",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("user_id", Integer, nullable=False),
#     Column("status", Integer, nullable=False),
#     Column("total_price", Integer, nullable=False),
#     Column("order_date", String),
#     Column("destination_name", String(100)),
#     Column("destination_email", String(100)),
#     Column("destination_zipcode", String(8)),
#     Column("destination_tel", String(200)),
#     Column("delivery_time", String(15)),
#     Column("payment_method", Integer)
# )

# order_items = Table(
#     "order_items",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("item_id", Integer, nullable=False),
#     Column("order_id", Integer, nullable=False),
#     Column("quantity", Integer, nullable=False),
#     Column("size", String(1))
#     # def getToppingList()

#     # def subtotal(this.id)
#     #     # with open('documents/cart_')
#     #     subTotal = 0
#     #     oneTotal = 0

# )

# order_toppings = Table(
#     "order_toppings",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("topping_id", Integer, nullable=False),
#     Column("order_item_id", Integer, nullable=False),
# )
