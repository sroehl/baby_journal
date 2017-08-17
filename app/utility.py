from .models import InventoryFormula, InventoryDiapers
from flask_login import current_user
from app import db
import datetime


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


def sort_array_by_date(orig_array):
    new_array = []
    while len(orig_array) > 0:
        if len(orig_array) > 1:
            lowest_date = parse_date(orig_array[0].date)
            lowest_idx = 0
            for i in range(1, len(orig_array)):
                next_date = parse_date(orig_array[i].date)
                if next_date < lowest_date:
                    lowest_date = next_date
                    lowest_idx = i
            new_array.insert(0, orig_array[lowest_idx])
            orig_array.pop(lowest_idx)
        else:
            if len(orig_array) == 1:
                new_array.insert(0, orig_array[0])
                orig_array.pop(0)
    return new_array


def parse_date(date):
    return datetime.datetime.strptime(date, '%I:%M%p on %m/%d/%y')
