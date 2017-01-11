from app import app, api, login_manager, bcrypt, db
from flask import render_template, redirect, url_for, session, flash, request, jsonify
from flask_login import login_required, login_user, logout_user, current_user

from flask_bcrypt import Bcrypt
from .models import User, Diaper, Bottle, Child, InventoryDiapers, InventoryFormula
from .forms import LoginForm

import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('overview.html')


@app.route('/diapers')
@login_required
def diapers():
    child = Child.query.filter_by(user_id=current_user.id).first()
    diapers = Diaper.query.filter_by(child_id=child.child_id).order_by(Diaper.date.desc())[0:30]
    sizes = [{'size': '1'}, {'size': '2'}, {'size': '3'}, {'size': '4'}, {'size': '5'}]
    if len(diapers) > 0:
        sizes[diapers[0].diaper_size - 1]['selected'] = 'selected'
    return render_template('diapers.html', child_name=child.child_name, diapers=diapers, sizes=sizes)


@app.route('/bottles')
@login_required
def bottles():
    child = Child.query.filter_by(user_id=current_user.id).first()
    bottles = Bottle.query.filter_by(child_id=child.child_id).order_by(Bottle.date.desc())[0:30]
    return render_template('bottles.html', child_name=child.child_name, bottles=bottles)


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
    size = request.form['size']
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
    date = request.form['date']
    size = request.form['size']
    diaper_size = request.form['diaper_size']
    diaper_type = request.form['diaper_type']
    diaper = Diaper(child.child_id, date, size, diaper_type, diaper_size)
    db.session.add(diaper)
    db.session.flush()
    db.session.commit()
    change_diaper_inventory(diaper_size, -1)
    return redirect(url_for('diapers'))


@app.route('/add_bottle', methods=['POST'])
@login_required
def add_bottle():
    child = Child.query.filter_by(user_id=current_user.id).first()
    date = request.form['date']
    amount = int(request.form['amount'])
    bottle = Bottle(child.child_id, date, amount)
    db.session.add(bottle)
    db.session.flush()
    db.session.commit()
    change_formula_inventory(amount * -1)
    return redirect(url_for('bottles'))


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
    #result = Diaper.query.filter_by(id=request.form['id']).delete()
    result = Diaper.query.filter_by(id=request.form['id']).delete()
    db.session.commit()
    return jsonify({"result": result})


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if Bcrypt.check_password_hash(None, pw_hash=user.password, password=form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid login.  Please login again')
                return redirect(url_for('login'))
        else:
          flash('Invalid login.  Please login again')
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login.html', form=LoginForm())


def change_formula_inventory(amount):
    formula = InventoryFormula.query.filter_by(user_id=current_user.id).first()
    if formula:
        formula.amount = formula.amount + amount
    else:
        inv_formula = InventoryFormula(current_user.id, amount)
        db.session.add(inv_formula)
    db.session.commit()


def change_diaper_inventory(size, amount):
    if amount is str:
        amount = int(amount)
    if size is str:
        size = int(size)
    diaper = InventoryDiapers.query.filter_by(user_id=current_user.id, size=size).first()
    if diaper:
        diaper.amount = diaper.amount + amount
    else:
        inv_diaper = InventoryDiapers(current_user.id, size, amount)
        db.session.add(inv_diaper)
    db.session.commit()