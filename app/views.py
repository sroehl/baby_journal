from app import app, login_manager, bcrypt, db, api
from flask import render_template, redirect, url_for, session, flash, request, jsonify, abort
from flask_login import login_required, login_user, logout_user, current_user

from flask_bcrypt import Bcrypt
from .models import User, Diaper, Bottle, Child, Food
from .forms import LoginForm, RegisterForm
from .stats import get_stats, run_update
from .utility import *


@app.route('/')
@app.route('/stats')
@login_required
def index():
    child = Child.query.filter_by(user_id=current_user.id).first()
    json_stats = get_stats(child.child_id)
    return render_template('stats.html', stats=json_stats)


@app.route('/diapers')
@login_required
def diapers():
    child = Child.query.filter_by(user_id=current_user.id).first()
    diapers = Diaper.query.filter_by(child_id=child.child_id).order_by(Diaper.date.desc())[0:30]
    for diaper in diapers:
        diaper.date = diaper.date.strftime("%I:%M%p on %m/%d/%y")
    sizes = [{'size': '0'}, {'size': '1'}, {'size': '2'}, {'size': '3'}, {'size': '4'}, {'size': '5'}]
    if len(diapers) > 0:
        sizes[diapers[0].diaper_size]['selected'] = 'selected'
    return render_template('diapers.html', child_name=child.child_name, diapers=diapers, sizes=sizes)


@app.route('/bottles')
@login_required
def bottles():
    child = Child.query.filter_by(user_id=current_user.id).first()
    bottles = Bottle.query.filter_by(child_id=child.child_id).order_by(Bottle.date.desc())[0:30]
    foods = Food.query.filter_by(child_id=child.child_id).order_by(Food.date.desc())[0:30]
    allFood = []
    for bottle in bottles:
        bottle.date = bottle.date.strftime("%I:%M%p on %m/%d/%y")
        bottle.type = "bottle"
        allFood.append(bottle)
    for food in foods:
        food.date = food.date.strftime("%I:%M%p on %m/%d/%y")
        food.type = 'food'
        allFood.append(food)
    allFoodSorted = sort_array_by_date(allFood)
    return render_template('bottles.html', child_name=child.child_name, foods=allFoodSorted)


@app.route('/inventory')
@login_required
def inventory():
    inv_diapers = InventoryDiapers.query.filter_by(user_id=current_user.id).order_by(InventoryDiapers.size)
    inv_formula = InventoryFormula.query.filter_by(user_id=current_user.id).first()
    return render_template('inventory.html', diapers=inv_diapers, formula=inv_formula)


@app.route('/add_inventory_diapers', methods=['POST'])
@login_required
def add_inventory_diapers():
    amount = int(request.form['amount'])
    size = int(request.form['size'])
    change_diaper_inventory(size, amount)
    return redirect(url_for('inventory'))


@app.route('/add_inventory_formula', methods=['POST'])
@login_required
def add_inventory_formula():
    amount = int(request.form['amount'])
    change_formula_inventory(amount)
    return redirect(url_for('inventory'))


@app.route('/add_diaper', methods=['POST'])
@login_required
def add_diaper():
    child = Child.query.filter_by(user_id=current_user.id).first()
    date = parse_request_date(request.form['date'])
    size = request.form['size']
    diaper_size = request.form['diaper_size']
    diaper_type = request.form['diaper_type']
    diaper = Diaper(child.child_id, date, size, diaper_type, diaper_size)
    db.session.add(diaper)
    db.session.flush()
    db.session.commit()
    change_diaper_inventory(diaper_size, -1)
    run_update(child.child_id)
    return redirect(url_for('diapers'))


@app.route('/add_bottle', methods=['POST'])
@login_required
def add_bottle():
    child = Child.query.filter_by(user_id=current_user.id).first()
    date = parse_request_date(request.form['date'])
    if request.form['submit'] == 'bottle':
        amount = float(request.form['amount'])
        change_formula_inventory(amount * -1)
    else:
        amount = -1
    bottle = Bottle(child.child_id, date, amount)
    db.session.add(bottle)
    db.session.flush()
    db.session.commit()
    run_update(child.child_id)
    return redirect(url_for('bottles'))


@app.route('/add_solid', methods=['POST'])
@login_required
def add_solid():
    child = Child.query.filter_by(user_id=current_user.id).first()
    date = parse_request_date(request.form['date'])
    name = request.form['foodname']
    food = Food(child.child_id, date, name)
    db.session.add(food)
    db.session.flush()
    db.session.commit()
    return redirect(url_for('bottles'))


@app.route('/delete_solid', methods=['POST'])
@login_required
def delete_solid():
    result = Food.query.filter_by(id=request.form['id']).delete()
    db.session.commit()
    return jsonify({"result": result})


@app.route('/delete_bottle', methods=['POST'])
@login_required
def delete_bottle():
    bottle = Bottle.query.filter_by(id=request.form['id']).first()
    change_formula_inventory(bottle.amount)
    result = Bottle.query.filter_by(id=request.form['id']).delete()
    db.session.commit()
    return jsonify({"result": result})


@app.route('/delete_diaper', methods=['POST'])
@login_required
def delete_diaper():
    diaper = Diaper.query.filter_by(id=request.form['id']).first()

    change_diaper_inventory(diaper.diaper_size, 1)
    result = Diaper.query.filter_by(id=request.form['id']).delete()
    db.session.commit()
    return jsonify({"result": result})


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


@login_manager.header_loader
def load_user_from_header(header_val):
    return User.query.filter_by(api_key=header_val).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if Bcrypt.check_password_hash(None, pw_hash=user.password, password=form.password.data):
                login_user(user, remember=True)
                target = request.args.get('next')
                print(target)
                if target == '/logout':
                    target = None
                return redirect(target or url_for('index'))
            else:
                flash('Invalid login.  Please login again')
                return redirect(url_for('login'))
        else:
            flash('Invalid login.  Please login again')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')
        email = form.email.data
        child_name = form.child_name.data
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash("Username or email already registered")
            return render_template('register.html', form=form)
        user = User(username, password, email)
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        child = Child(user.id, child_name)
        db.session.add(child)
        db.session.flush()
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login.html', form=LoginForm())

