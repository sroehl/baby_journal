from app import app, db
from flask import request, jsonify
from .models import User, Diaper, Bottle, Child, InventoryDiapers, InventoryFormula
from .utility import change_diaper_inventory, change_formula_inventory
from flask_login import login_required, current_user
from datetime import datetime
from dateutil import parser


@app.route('/api/request_token')
@login_required
def request_token():
    user = User.query.get(current_user.id)
    token = user.generate_auth_token()
    db.session.commit()
    return token


@app.route('/api/diaper', methods=['POST', 'GET'])
@login_required
def api_diaper():
    if request.method == 'GET':
        count = get_count_arg(request.args)
        child = Child.query.filter_by(user_id=current_user.id).first()
        diapers = Diaper.query.filter_by(child_id=child.child_id).order_by(Diaper.date.desc())[0:count]
        diapers_json = []
        for diaper in diapers:
            diapers_json.append(diaper.serialize)
        return jsonify(diapers_json)
    elif request.method == 'POST':
        data = request.get_json(force=True)
        if 'size' in data and 'type' in data:
            child = Child.query.filter_by(user_id=current_user.id).first()
            if 'date' in data:
                p = parser.parser()
                date = p.parse(data['date'])
            else:
                date = datetime.now()
            if 'diaper_size' in data:
                diaper_size = data['diaper_size']
            else:
                last_diaper = Diaper.query.filter_by(child_id=child.child_id).order_by(Diaper.date.desc()).first()
                if last_diaper is not None:
                    diaper_size = last_diaper.diaper_size
                else:
                    diaper_size = 1
            size = data['size']
            diaper_type = data['type']
            diaper = Diaper(child.child_id, date, size, diaper_type, diaper_size)
            db.session.add(diaper)
            db.session.flush()
            db.session.commit()
            change_diaper_inventory(diaper_size, -1)
            return jsonify(diaper.serialize)


@app.route('/api/bottle', methods=['POST', 'GET'])
@login_required
def api_bottle():
    if request.method == 'GET':
        count = get_count_arg(request.args)
        child = Child.query.filter_by(user_id=current_user.id).first()
        bottles = Bottle.query.filter_by(child_id=child.child_id).order_by(Bottle.date.desc())[0:count]
        bottles_json = []
        for bottle in bottles:
            bottles_json.append(bottle.serialize)
        return jsonify(bottles_json)
    elif request.method == 'POST':
        data = request.get_json(force=True)
        if 'amount' in data:
            child = Child.query.filter_by(user_id=current_user.id).first()
            if 'date' in data:
                p = parser.parser()
                date = p.parse(data['date'])
            else:
                date = datetime.now()
            amount = data['amount']
            bottle = Bottle(child.child_id, date, amount)
            db.session.add(bottle)
            db.session.flush()
            db.session.commit()
            change_formula_inventory(amount)
            return jsonify(bottle.serialize)


@app.route('/api/inventory/bottle', methods=['POST', 'GET'])
@login_required
def api_inventory_bottle():
    if request.method == 'GET':
        inv_bottle = InventoryFormula.query.filter_by(user_id=current_user.id).first()
        if inv_bottle is not None:
            amount = inv_bottle.amount
        else:
            amount = 0
        return jsonify({'amount': amount})
    elif request.method == 'POST':
        data = request.get_json(force=True)
        if 'amount' in data:
            amount = change_formula_inventory(data['amount'])
            return jsonify({'amount': amount})


@app.route('/api/inventory/diaper', methods=['POST', 'GET'])
@login_required
def api_inventory_diaper():
    if request.method == 'GET':
        inv_diapers = InventoryDiapers.query.filter_by(user_id=current_user.id).order_by(InventoryDiapers.size)
        diapers_json = {}
        for diaper in inv_diapers:
            diapers_json[diaper.size] = diaper.amount
        return jsonify(diapers_json)
    elif request.method == 'POST':
        data = request.get_json(force=True)
        if 'amount' in data and 'size' in data:
            amount = change_diaper_inventory(data['size'], data['amount'])
            return jsonify({'size': data['size'], 'amount': amount})


def get_count_arg(args):
    if args.get('count') is not None:
        count = int(args.get('count'))
    else:
        count = 20
    return count
