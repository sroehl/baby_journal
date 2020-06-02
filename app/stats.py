import threading

from app import db, models
from sqlalchemy import func, and_, Date, cast
from datetime import timedelta, datetime

DAILY_BOTTLES = 0
YESTERDAY_BOTTLES = 1
WEEKLY_BOTTLES = 2
WEEK_DAY_BOTTLES = 3

DAILY_DIAPERS = 100
YESTERDAY_DIAPERS = 101
WEEKLY_DIAPERS = 102
WEEK_DAY_DIAPERS = 103


STAT_DESCRITPIONS={
    DAILY_BOTTLES: 'Ounces Today',
    YESTERDAY_BOTTLES: 'Ounces Yesterday',
    WEEKLY_BOTTLES: 'Ounces for the Week',
    WEEK_DAY_BOTTLES: 'Average Ounces Per Day',
    DAILY_DIAPERS: 'Diapers Today',
    WEEKLY_DIAPERS: 'Diapers for the Week',
    WEEK_DAY_DIAPERS: 'Average Diapers Per Day',
    YESTERDAY_DIAPERS: 'Diapers Yesterday'
}


def add_stat(child_id, stat_id, value):
    stat = models.Stats.query.filter(and_((models.Stats.child_id==child_id),
                                             (models.Stats.stat_id==stat_id))).first()
    # Set value to 0 so null is not inserted
    if value is None:
        value = 0
    if stat is None:
        stat = models.Stats(child_id, stat_id, value)
    stat.value = value
    db.session.add(stat)
    db.session.flush()
    db.session.commit()


def daily_bottles(child_id):
    query = db.session.query(func.sum(models.Bottle.amount)).filter(and_(models.Bottle.child_id == child_id),
                                                                    (func.date(
                                                                        models.Bottle.date) == datetime.today().date()),
                                                                    (models.Bottle.amount > 0))
    result = query.all()[0]
    if result is not None and result[0] is not None:
        add_stat(child_id, DAILY_BOTTLES, result[0])


def yesterday_bottles(child_id):
    query = db.session.query(func.sum(models.Bottle.amount)).filter(and_(models.Bottle.child_id == child_id),
                                                                    (func.date(models.Bottle.date) == (
                                                                                datetime.today() - timedelta(
                                                                            days=1)).date()),
                                                                    (models.Bottle.amount > 0))
    result = query.all()[0]
    if result is not None and result[0] is not None:
        add_stat(child_id, YESTERDAY_BOTTLES, result[0])


def weekly_bottles(child_id):
    query = db.session.query(func.sum(models.Bottle.amount)).filter(and_(models.Bottle.child_id == child_id),
                                                                    (func.date(models.Bottle.date) > (
                                                                                datetime.today() - timedelta(
                                                                            days=8)).date()),
                                                                    (func.date(models.Bottle.date) != (
                                                                        datetime.today().date())),
                                                                    (models.Bottle.amount > 0))
    result = query.all()[0]
    if result is not None and result[0] is not None:
        add_stat(child_id, WEEKLY_BOTTLES, result[0])


def week_day_bottles(child_id):
    query = db.session.query(func.sum(models.Bottle.amount)).filter(and_(models.Bottle.child_id == child_id),
                                                                    (func.date(models.Bottle.date) > (
                                                                                datetime.today() - timedelta(
                                                                            days=8)).date()),
                                                                    (func.date(models.Bottle.date) != (
                                                                        datetime.today().date())),
                                                                    (models.Bottle.amount > 0))
    result = query.all()[0]
    if result is not None and result[0] is not None:
        add_stat(child_id, WEEK_DAY_BOTTLES, round(result[0] / 7, 2))


def daily_diapers(child_id):
    query = db.session.query(func.count(models.Diaper.date)).filter(and_(models.Diaper.child_id == child_id),
                                                                    (func.date(
                                                                        models.Diaper.date) == datetime.today().date()))
    result = query.all()[0]
    if result is not None and result[0] is not None:
        add_stat(child_id, DAILY_DIAPERS, result[0])


def weekly_diapers(child_id):
    query = db.session.query(func.count(models.Diaper.date)).filter(and_(models.Diaper.child_id == child_id),
                                                                    (func.date(models.Diaper.date) > (
                                                                                datetime.today() - timedelta(
                                                                            days=8)).date()),
                                                                    (func.date(models.Diaper.date) != (
                                                                        datetime.today().date())))
    result = query.all()[0]
    if result is not None and result[0] is not None:
        add_stat(child_id, WEEKLY_DIAPERS, result[0])


def week_day_diapers(child_id):
    query = db.session.query(func.count(models.Diaper.date)).filter(and_(models.Diaper.child_id == child_id),
                                                                    (func.date(models.Diaper.date) > (
                                                                                datetime.today() - timedelta(
                                                                            days=8)).date()),
                                                                    (func.date(models.Diaper.date) != (
                                                                        datetime.today().date())))
    result = query.all()[0]
    if result is not None and result[0] is not None:
        add_stat(child_id, WEEK_DAY_DIAPERS, round(result[0] / 7, 0))


def yesterday_diapers(child_id):
    query = db.session.query(func.count(models.Diaper.date)).filter(and_(models.Diaper.child_id == child_id),
                                                                    (func.date(models.Diaper.date) == (
                                                                                datetime.today() - timedelta(
                                                                            days=1)).date()))
    result = query.all()[0]
    if result is not None and result[0] is not None:
        add_stat(child_id, YESTERDAY_DIAPERS, result[0])


def run_update(child_id):
    thread = threading.Thread(target=update_stats, args=(child_id,))
    thread.start()


def update_stats(child_id):
    #  Bottle section
    daily_bottles(child_id)
    yesterday_bottles(child_id)
    weekly_bottles(child_id)
    week_day_bottles(child_id)
    #  Diaper Section
    daily_diapers(child_id)
    yesterday_diapers(child_id)
    weekly_diapers(child_id)
    week_day_diapers(child_id)


def get_stats(child_id):
    json_stats = []
    stats = models.Stats.query.filter(models.Stats.child_id==child_id)
    for stat in stats:
        json_stats.append({'description': STAT_DESCRITPIONS[stat.stat_id],
                           'value': stat.value})
    return json_stats

#  This is only used for testing
if __name__ == '__main__':
    update_stats(7)
