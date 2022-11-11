import psycopg2


class DataBase:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="",
            user="",
            password="",
            host="localhost",
            port=5432
        )
        self.con.autocommit = True
        self.cur = self.con.cursor()

    def get_user_by_email(self, email):
        self.cur.execute("SELECT * from users WHERE email = '{email}'")
        return self.cur.fetchone()

    def get_user_by_id(self, id):
        self.cur.execute("SELECT * from users WHERE id = '{id}'")
        return self.cur.fetchone()

    def all_products(self):
        self.cur.execute("SELECT * from products")
        return self.cur.fetchall()

    def get_product_by_id(self, id):
        self.cur.execute("SELECT * from products WHERE id = '{id}'")
        return self.cur.fetchone()
