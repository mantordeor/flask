from flask import Flask, render_template, jsonify, request, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from registerdb import db
from Flask_Form import FormRegister, FormLogin
from Flask_Form import UserReister, add_item
from model import UserReister, Product
import sqlite3
import bcrypt
import json

##pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + r"C:\Users\CPEB\Desktop\hw\registers.sqlite"

app.config['SECRET_KEY']='your key'


bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    
    return UserReister.query.get(int(user_id))

@app.route('/',methods=['GET','POST'])
def homepage():
    if request.method == 'POST':
        if 'Login' in request.form:
            return redirect('login')
        elif 'Signup' in request.form:
            return redirect('Signup')
    return render_template('index.html')

@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('product_interface.html', products = products)

@app.route('/Signup',methods=['GET', 'POST'])
def register():
    form = FormRegister()
    try:
        if form.validate_on_submit():
            user = UserReister(
                username = form.username.data,
                email = form.email.data,
                password = form.password.data
            )
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        return render_template('register.html', form=form)
    except Exception as e:
        print(e)
        return jsonify({'code': -1, 'error_message': str(e)})

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        user = UserReister.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user, form.remember_me.data)
                next = request.args.get('homepage')
                if not next_is_valid(next):
                    return 'Bad Boy!!'
                return redirect(next or '/')
            else:
                flash('Wrong Email or Password')
        else:
            flash('Wrong Email or Password')
    return render_template('login.html', form=form)

def next_is_valid(url):
    return True

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Weee')
    return redirect('/')

@app.route('/add_product',methods=['GET','POST'])
def add_product():
    form = add_item()
    try:
        if form.validate_on_submit():
            item = Product(
                item_name = form.item_name.data,
                item_price = form.item_price.data
            )
            db.session.add(item)
            db.session.commit()
            return redirect('add_product')
        return render_template('add_Product.html', form=form)
    except Exception as e:
        print(e)
        return jsonify({'code': -1, 'error_message': str(e)})

@app.route('/userbought', methods=['POST'])
def do_buy():
    try:
        if current_user.is_authenticated:
            item_id = request.form.get('item_id')
            user = UserReister.query.filter_by(id=current_user.id).first()
            item_bought_list = json.loads(user.item_bought_id) if user.item_bought_id else []  # 解析购买列表字符串为列表
            item_bought_list.append(item_id)  # 将新项目添加到列表中
            user.item_bought_id = json.dumps(item_bought_list)  # 将列表转换为字符串并保存回数据库
            db.session.commit()
            return redirect('shop')
        else:
            return redirect('login')
    except Exception as e:
        print(e)
        return jsonify({'code': -1, 'error_message': str(e)})
    
@app.route('/cart', methods=['GET', 'POST'])
def view_cart():
    if current_user.is_authenticated:
        user = UserReister.query.filter_by(username=current_user.username).first()
        if user:
            item_ids_str = user.item_bought_id  # 获取字符串形式的item_ids
            item_ids_list = json.loads(item_ids_str)  # 反序列化为实际列表
            if len(item_ids_list) > 0:
                items_in_cart = Product.query.filter(Product.id.in_(item_ids_list)).all()
                return render_template('UserCart.html', cart=items_in_cart)
    return render_template('UserCart.html', cart=None)


@app.route('/serch')
def serch_data():
    from model import UserReister
    from Flask_Form import FormRegister
    all_register = db.session.query(UserReister).all()
    print(all_register)
    for i in all_register:
        print(i)
    return 'Success, Please Check your database.'


if __name__ == '__main__':
    app.debug = True
    app.run()

        