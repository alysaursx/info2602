from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import csv


db =SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'alvins hot juice box'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, UserWorkout

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    from .models import User, Workout
    from werkzeug.security import generate_password_hash, check_password_hash
    if not path.exists('App/' + DB_NAME):
        with app.app_context():
            db.drop_all()
            db.create_all()
            bob = User(username="bob",email="bob@mail.com",password=generate_password_hash("bobpass", method='pbkdf2:sha256'))
            db.session.add(bob)
            db.session.commit()

            with open('exercises.csv', newline='', encoding='utf8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['secondaryMuscles'] == '':
                        row['secondaryMuscles'] = None
                    workout = Workout(name=row['name'], force=row['force'], level=row['level'], mechanic=row['mechanic'], equipment=row['equipment'], primaryMuscles=row['primaryMuscles'], secondaryMuscles=row['secondaryMuscles'], instructions=row['instructions'], category=row['category'], id=row['id'], image1=row['Image1'], image2=row['Image2'])
                    #print(row['Image1'])
                    db.session.add(workout)            
                db.session.commit()
        print('Created database!')




