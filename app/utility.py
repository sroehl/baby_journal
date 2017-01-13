from .models import InventoryFormula, InventoryDiapers
from flask_login import current_user
from app import db


def change_formula_inventory(amount):
    return_amount = amount
    formula = InventoryFormula.query.filter_by(user_id=current_user.id).first()
    if formula:
        formula.amount = formula.amount + amount
        return_amount = formula.amount
    else:
        inv_formula = InventoryFormula(current_user.id, amount)
        db.session.add(inv_formula)
    db.session.commit()
    return return_amount


def change_diaper_inventory(size, amount):
    return_amount = amount
    diaper = InventoryDiapers.query.filter_by(user_id=current_user.id, size=size).first()
    if diaper:
        diaper.amount = diaper.amount + amount
        return_amount = diaper.amount
    else:
        inv_diaper = InventoryDiapers(current_user.id, size, amount)
        db.session.add(inv_diaper)
    db.session.commit()
    return return_amount
