from flask import Flask, render_template, request, make_response, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db_utility import DataBase

app = Flask(__name__)
app.config['SECRET_KEY'] = '1zZUwWyKXeZln_OKHhiRkw'

db = DataBase()


@app.route('/', methods=['GET', 'POST'])
def main():
    context = {
        'title': 'SakuraStore'
    }
    return render_template("main.html", **context)


if __name__ == '__main__':
    app.run()
