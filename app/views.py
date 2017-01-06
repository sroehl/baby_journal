from app import app, api, login_manager, bcrypt, db
from flask import render_template, redirect, url_for, session, flash, request, jsonify
from flask_login import login_required, login_user, logout_user, current_user

from flask_bcrypt import Bcrypt
from .models import User, Diaper, Bottle, Child
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
    diapers = [{'size': 'big', 'type': 'pee', 'date': '1/2/2017 10:30:15', 'id': '12312'}]
    diapers = Diaper.query.filter_by(child_id=child.child_id).order_by(Diaper.date.desc())[0:30]
    return render_template('diapers.html', child_name=child.child_name, diapers=diapers)


@app.route('/bottles')
@login_required
def bottles():
    child = Child.query.filter_by(user_id=current_user.id).first()
    bottles = [{'amount': 4, 'date': '1/2/2016', 'id': '111'}]
    bottles = Bottle.query.filter_by(child_id=child.child_id).order_by(Bottle.date.desc())[0:30]
    return render_template('bottles.html', child_name=child.child_name, bottles=bottles)


@app.route('/food')
@login_required
def food():
    return render_template('food.html')


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/add_diaper', methods=['POST'])
@login_required
def add_diaper():
    child = Child.query.filter_by(user_id=current_user.id).first()
    date = request.form['date']
    size = request.form['diaper_size']
    diaper_type = request.form['diaper_type']
    diaper = Diaper(child.child_id, date, size, diaper_type)
    db.session.add(diaper)
    db.session.flush()
    db.session.commit()
    return redirect(url_for('diapers'))


@app.route('/add_bottle', methods=['POST'])
@login_required
def add_bottle():
    child = Child.query.filter_by(user_id=current_user.id).first()
    date = request.form['date']
    amount = request.form['amount']
    bottle = Bottle(child.child_id, date, amount)
    db.session.add(bottle)
    db.session.flush()
    db.session.commit()
    return redirect(url_for('bottles'))


@app.route('/delete_bottle', methods=['POST'])
@login_required
def delete_bottle():
    result = Bottle.query.filter_by(id=request.form['id']).delete()
    db.session.commit()
    return jsonify({"result": result})


@app.route('/delete_diaper', methods=['POST'])
@login_required
def delete_diaper():
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
