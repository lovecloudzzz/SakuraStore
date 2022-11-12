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
        UserDB.cur.execute("SELECT * FROM users WHERE email = '%s'" % email)
        return UserDB.cur.fetchone()


class ProductDB(BaseDB):
    @classmethod
    def all_products(cls):
        ProductDB.cur.execute("SELECT * from products")
        return ProductDB.cur.fetchall()

    @classmethod
    def get_product_by_id(cls, id):
        ProductDB.cur.execute("SELECT * from products WHERE id = '{id}'")
        return ProductDB.cur.fetchone()

    @classmethod
    def delete_product_by_id(cls, id):
        ProductDB.cur.execute("DELETE FROM products WHERE id = '%s'" % id)


class OrdersDB(BaseDB):
    @classmethod
    def all_orders(cls):
        OrdersDB.cur.execute("SELECT * from products")
        return OrdersDB.cur.fetchall()

    @classmethod
    def get_order_by_id(cls, id):
        OrdersDB.cur.execute("SELECT * from products WHERE id = '{id}'")
        return OrdersDB.cur.fetchone()


class FavoritesDB(BaseDB):
    @classmethod
    def all_favorites(cls):
        FavoritesDB.cur.execute("SELECT * from favorites")
        return FavoritesDB.cur.fetchall()

    @classmethod
    def add_favorite(cls, user_id, product_id):
        FavoritesDB.cur.execute("INSERT INTO favorites (user_id, product_id) VALUES (%s, %s)" % (user_id, product_id))

    @classmethod
    def remove_favorite(cls, user_id, product_id):
        FavoritesDB.cur.execute("DELETE FROM favorites WHERE user_id = %s and product_id = %s" % (user_id, product_id))

    @classmethod
    def get_all_favourites(cls, user_id):
        FavoritesDB.cur.execute("SELECT id, title, annotation FROM products JOIN favorites f "
                         "ON products.id = f.product_id "
                         "WHERE user_id = %s" % user_id)
        return FavoritesDB.cur.fetchall()


class CartDB(BaseDB):
    @classmethod
    def all_favorites(cls):
        CartDB.cur.execute("SELECT * from carts")
        return CartDB.cur.fetchall()

    @classmethod
    def get_favorite_by_id(cls, id):
        CartDB.cur.execute("SELECT * from carts WHERE id = '{id}'")
        return CartDB.cur.fetchone()


class OrdersProductsDB(BaseDB):
    @classmethod
    def all_favorites(cls):
        OrdersProductsDB.cur.execute("SELECT * from orders_products")
        return OrdersProductsDB.cur.fetchall()

    @classmethod
    def get_favorite_by_id(cls, id):
        OrdersProductsDB.cur.execute("SELECT * from orders_products WHERE id = '{id}'")
        return OrdersProductsDB.cur.fetchone()

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
        return True if self.__user[0] else False

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        return self.__user[4]