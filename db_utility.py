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

    def prepare_data(self, data):
        res_data = []
        if len(data):
            column_names = [desc[0] for desc in self.cur.description]
            for row in data:
                res_data += [{c_name: row[key] for key, c_name in enumerate(column_names)}]
        return res_data

    def get_user_by_email(self, email):
        self.cur.execute("SELECT * from local.users WHERE email = '{email}'")
        return self.prepare_data(self.cur.fetchall())[0]

    def get_user_by_id(self, id):
        self.cur.execute("SELECT * from database.users WHERE id = '{id}'")
        return self.prepare_data(self.cur.fetchall())[0]

    def all_products(self):
        self.cur.execute("SELECT * from database.products")
        return self.prepare_data(self.cur.fetchall())

    def get_product_by_id(self, id):
        self.cur.execute("SELECT * from database.products WHERE id = '{id}'")
        return self.prepare_data(self.cur.fetchall())[0]
