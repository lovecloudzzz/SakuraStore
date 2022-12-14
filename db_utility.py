import psycopg2


class BaseDB:
    def __init__(self):
        pass
    con = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="",
        host="localhost",
        port=5432
    )
    con.autocommit = True
    cur = con.cursor()


class UserDB(BaseDB):
    @classmethod
    def register_user(cls, login, email, password):
        UserDB.cur.execute(
            "INSERT INTO users (login, email, password) VALUES (%s, %s, %s)",
            (login, email, password))

    @classmethod
    def get_user_by_id(cls, id):
        UserDB.cur.execute(f"SELECT * from users WHERE id = {id}")
        return UserDB.cur.fetchone()

    @classmethod
    def get_user_by_login(cls, login):
        UserDB.cur.execute("SELECT * from users WHERE login = '%s'" % login)
        return UserDB.cur.fetchone()

    @classmethod
    def get_user_by_email(cls, email):
        try:
            UserDB.cur.execute("SELECT * FROM users WHERE email = '%s'" % email)
            res = UserDB.cur.fetchone()
            if not res:
                return False
            return res
        except Exception as e:
            print(e)
            return False

    @classmethod
    def update(cls, user_id, login, password):
        UserDB.cur.execute("UPDATE users SET login='%s', password='%s' WHERE id='%s'" % (login, password, user_id))


class ProductDB(BaseDB):
    @classmethod
    def update(cls,id,title,annotation,tags,price):
        UserDB.cur.execute("UPDATE prodicts SET title='%s', annotation='%s', tags='%s', price='%s' WHERE id='%s'" % (title, annotation, tags, price, id))

    @classmethod
    def all_products(cls):
        ProductDB.cur.execute("SELECT * from products")
        return ProductDB.cur.fetchall()

    @classmethod
    def products_by_tags(cls, products_tags):
        ProductDB.cur.execute("SELECT * from products where '%s' && tags" % products_tags)
        return ProductDB.cur.fetchall()

    @classmethod
    def get_product_by_id(cls, id):
        ProductDB.cur.execute("SELECT * from products WHERE id = '%s'" % id)
        return ProductDB.cur.fetchone()

    @classmethod
    def delete_product_by_id(cls, id):
        ProductDB.cur.execute("DELETE FROM products WHERE id = '%s'" % id)

    @classmethod
    def add_product(cls, title, annotation, tags, banner_link, price):
        print(title, annotation, tags, banner_link, price)
        ProductDB.cur.execute("INSERT INTO products(title, annotation, tags, banner_link, price) VALUES (%s, %s, %s, %s, %s)", (title, annotation, tags, banner_link, price))


class FavoritesDB(BaseDB):
    @classmethod
    def check(cls,user_id, product_id):
        res = FavoritesDB.cur.execute("SELECT * from favorites WHERE user_id = '%s' and product_id = '%s'" % (user_id, product_id))
        return bool(FavoritesDB.cur.fetchone())

    @classmethod
    def add_favorite(cls, user_id, product_id):
        FavoritesDB.cur.execute("INSERT INTO favorites (user_id, product_id) VALUES (%s, %s)" % (user_id, product_id))

    @classmethod
    def remove_favorite(cls, product_id):
        FavoritesDB.cur.execute("DELETE FROM favorites WHERE product_id = '%s'" % product_id)

    @classmethod
    def remove_one_favorite(cls, user_id, product_id):
        FavoritesDB.cur.execute("DELETE FROM favorites WHERE user_id = '%s' and product_id = '%s'" % (user_id, product_id))

    @classmethod
    def get_all_favorites(cls, user_id):
        ProductDB.cur.execute("SELECT * FROM products JOIN favorites as f ON products.id = f.product_id WHERE user_id = '%s'" % user_id)
        return ProductDB.cur.fetchall()


class CartDB(BaseDB):
    @classmethod
    def get_cart(cls, user_id):
        CartDB.cur.execute("SELECT title, banner_link, price, products.id FROM products JOIN carts as f ON products.id = f.product_id WHERE user_id = '%s'" % user_id)
        return CartDB.cur.fetchall()

    @classmethod
    def clear_cart(cls, user_id):
        CartDB.cur.execute("DELETE FROM carts WHERE user_id = '%s'" % user_id)

    @classmethod
    def add_to_cart(cls, user_id, product_id):
        CartDB.cur.execute("INSERT INTO carts (user_id, product_id) VALUES (%s, %s)" % (user_id, product_id))

    @classmethod
    def delete_from_cart(cls, user_id, product_id):
        CartDB.cur.execute("DELETE FROM carts WHERE user_id = '%s' and product_id = '%s'" % (user_id, product_id))

    @classmethod
    def check_cart(cls, user_id):
        CartDB.cur.execute("SELECT title, banner_link, price, products.id FROM products JOIN carts as f ON products.id = f.product_id WHERE user_id = '%s'" % user_id)
        return bool(CartDB.cur.fetchall())


class OrdersDB(BaseDB):
    @classmethod
    def all_orders(cls, user_id):
        OrdersDB.cur.execute("SELECT id from orders where user_id = '%s'" % user_id)
        return OrdersDB.cur.fetchall()

    @classmethod
    def new_order_id(cls):
        OrdersDB.cur.execute("SELECT id FROM orders ORDER BY id DESC")
        return OrdersDB.cur.fetchone()[0] + 1

    @classmethod
    def create_order(cls, user_id):
        products = CartDB.get_cart(user_id)
        order_id = OrdersDB.new_order_id()
        OrdersDB.cur.execute("INSERT INTO orders (user_id, id) VALUES (%s, %s)" % (user_id, order_id))
        for product in products:
            OrdersProductsDB.cur.execute("INSERT INTO orders_products (product_id, order_id) VALUES (%s, %s)" % (product[3], order_id))
        CartDB.clear_cart(user_id)


class OrdersProductsDB(BaseDB):
    @classmethod
    def all_orders(cls, user_id):
        orders = OrdersDB.all_orders(user_id)
        res = []
        for order in orders:
            summa = 0
            OrdersProductsDB.cur.execute(
                "SELECT title, banner_link, price  FROM products JOIN (SELECT product_id, order_id FROM orders_products) op ON op.product_id = products.id WHERE order_id = %s" % order[0]
            )
            products = OrdersProductsDB.cur.fetchall()
            for product in products:
                summa += product[2]
            res.append(tuple((order[0], products, summa)))
        print(res)
        return res

    @classmethod
    def delete_by_id(cls, user_id, product_id):
        OrdersProductsDB.cur.execute("DELETE FROM orders_products (user_id, product_id) VALUES (%s, %s)" % (user_id, product_id))


class UserLogin:
    def fromDB(self, user_id):
        self.__user = UserDB.get_user_by_id(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user[0])

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        return self.__user[4]
