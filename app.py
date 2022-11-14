from flask import Flask, render_template, request, make_response, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db_utility import BaseDB, UserDB, ProductDB, FavoritesDB, CartDB, OrdersDB, OrdersProductsDB, UserLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = '1zZUwWyKXeZln_OKHhiRkw'
login_manager = LoginManager(app)
login_manager.login_view = 'register'


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/', methods=['GET', 'POST'])
def main():
    tags = ['cёнен', 'cэйнен', 'комедия', 'романтика', 'школа', 'военное', 'драма',
            'магия', 'космос', 'приключения', 'фантастика', 'фэнтези']
    products = ProductDB.all_products()
    context = {
        'title': 'SakuraStore',
        'products': products,
        'tags': tags
    }
    return render_template('main.html', **context)


@app.route('/add_to_fav/<int:id>', methods=['get'])
def add_to_fav(id):
    product_id = id
    user_id = current_user.get_id()
    CartDB.add_to_cart(user_id, product_id)
    return

@app.route('/add_to_cart/<int:id>', methods=['get'])
def add_to_cart():
    product_id = 1
    product_id = id
    user_id = current_user.get_id()
    if FavoritesDB.check(user_id, product_id):
         pass
    else:
        FavoritesDB.add_favorite(user_id, product_id)
    return {'img': '/static/css/assets/addedtofavorites'}

@login_required
@app.route('/add_manga', methods=['GET', 'POST'])
def add_manga():
    context = {
        'title': 'Добавить мангу',
    }
    is_admin = current_user.is_admin
    if is_admin:
        if request.method == 'POST':
            title = request.form.get('title')
            annotation = request.form.get('annotation')
            tags = request.form.get('tags')
            price = request.form.get('price')
            banner_link = request.form.get('banner_link')
            ProductDB.add_product(title,annotation,tags,banner_link,price)
            return redirect(url_for('add_manga'))
        else:
            return render_template('add_manga.html', **context)
    return redirect(url_for('main'))


@login_required
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        UserDB.update(current_user.get_id(), login, password)
    user = UserDB.get_user_by_id(current_user.get_id())
    context = {
        'title': 'Профиль',
        'login': user[1],
        'email': user[2],
        'password': user[3]
    }
    return render_template("profile.html", **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserDB.get_user_by_email(email)
        if user:
            if user[2] == email and user[3] == password:
                user_login = UserLogin().create(user)
                login_user(user_login, remember=False)
                return redirect('/')
            else:
                message = "Wrong username or password"
    context = {
        'title': 'Вход'
    }
    return render_template("login.html", **context)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = request.form.get('login')
        email = request.form.get('email')
        password = request.form.get('password')
        if UserDB.get_user_by_email(email):
            print('Пользователь уже создан по этой почте')
        else:
            UserDB.register_user(login, email, password)
            user = UserDB.get_user_by_email(email)
            user_login = UserLogin().create(user)
            login_user(user_login, remember=True)
            return redirect('/')
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