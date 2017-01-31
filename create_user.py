from app import app, db, models, bcrypt


def main():
    with app.app_context():
        db.metadata.drop_all(db.engine)
        db.metadata.create_all(db.engine)
        username = 'steve'
        password = bcrypt.generate_password_hash(password='test').decode('utf-8')
        email = 'sprzeo@gmail.com'
        user = models.User(username, password, email)
        print("Creating user")
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        print("Creating child")
        child = models.Child(user.id, 'Olive')
        db.session.add(child)
        db.session.flush()
        db.session.commit()

main()
