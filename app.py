from flask import Flask, render_template, request, make_response, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db_utility import BaseDB, UserDB, ProductDB, FavoritesDB, CartDB, OrdersDB, OrdersProductsDB

app = Flask(__name__)
app.config['SECRET_KEY'] = '1zZUwWyKXeZln_OKHhiRkw'
login_manager = LoginManager(app)
login_manager.login_view = 'register'


@login_manager.user_loader
def load_user(user_id):
    return UserDB().get_user_by_id(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))


@app.route('/', methods=['GET', 'POST'])
def main():
    context = {
        'title': 'SakuraStore',
        'products': ProductDB.all_products()
    }
    return render_template('main.html', **context)


@login_required
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    context = {
        'title': 'Профиль'
    }
    return render_template("profile.html", **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    context = {
        'title': 'Вход'
    }
    return render_template("login.html", **context)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    context = {
        'title': 'Регистрация'
    }
    return render_template("registration.html", **context)



@login_required
@app.route('/orders', methods=['GET', 'POST'])
def orders():
    context = {
        'title': 'Заказы'
    }
    return render_template("orders.html", **context)


@login_required
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    context = {
        'title': 'Корзина'
    }
    return render_template("cart.html", **context)


@login_required
@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    context = {
        'title': 'Избранное'
    }
    return render_template("favorites.html", **context)

if __name__ == '__main__':
    app.run()