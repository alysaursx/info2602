from . import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

#User
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  routine = db.relationship('UserWorkout', backref='user')

  def addWorkout(self, workout_id, workout_name, reps, sets):
    work = Workout.query.get(workout_id)
    if work:
        try:
            workout = UserWorkout(user_id=self.id, workout_id=workout_id, workout_name=work.name, workout_reps=reps, workout_sets=sets)
            db.session.add(workout)
            db.session.commit()
            return workout
        except Exception as e:
            print(e)
            db.session.rollback()
            return None
    return None

  def removeWorkout(self, workout_id):
    work = UserWorkout.query.get(workout_id)
    if work.user == self:
      db.session.delete(work)
      db.session.commit()
      return True
    return None

#    def removeWorkout(self, workout_name):
#    user_workout = UserWorkout.query.filter_by(user_id=self.id, workout_name=workout_name).first()
#    if not user_workout:
#      print(f"Error: workout {workout_name} not found in user's routine")
#      return None
#    try:
#      db.session.delete(user_workout)
#      db.session.commit()
#      print(f"Workout {workout_name} removed from user's routine")
#      return user_workout
#    except Exception as e:
#      print(f"Error removing workout: {e}")
#      db.session.rollback()
#      return None
#    

#Workouts
class Workout(db.Model):
  name = db.Column(db.String(80))
  force = db.Column(db.String(80))
  level = db.Column(db.String(80))
  mechanic = db.Column(db.String(80))
  equipment = db.Column(db.String(80))
  primaryMuscles = db.Column(db.String(80))
  secondaryMuscles = db.Column(db.String(120))
  instructions = db.Column(db.String(500))
  category = db.Column(db.String(80))
  id = db.Column(db.Integer, primary_key=True)
  image1 = db.Column(db.String(200))
  image2 = db.Column(db.String(200))

  def __init__(self, name, force, level, mechanic, equipment, primaryMuscles, secondaryMuscles, instructions, category, id, image1, image2):
    self.name = name
    self.force = force
    self.level = level
    self.mechanic = mechanic
    self.equipment = equipment
    self.primaryMuscles = primaryMuscles
    self.secondaryMuscles = secondaryMuscles
    self.instructions = instructions
    self.category = category
    self.id = id
    self.image1 = image1
    self.image2 = image2

  def get_json(self):
    return {
        'name': self.name,
        'force': self.force,
        'level': self.level,
        'mechanic': self.mechanic,
        'equipment': self.equipment,
        'primaryMuscles': self.primaryMuscles,
        'secondaryMuscles': self.secondaryMuscles,
        'instructions': self.instructions,
        'category': self.category,
        'id': self.id,
        'image1': self.image1,
        'image2': self.image2
    }

#User Routine
class UserWorkout(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
  workout = db.relationship('Workout')
  workout_name = db.Column(db.String(120))
  workout_reps = db.Column(db.Integer)
  workout_sets = db.Column(db.Integer)

  def __init__(self, user_id, workout_id, workout_name, workout_reps, workout_sets):
    self.user_id = user_id
    self.workout_id = workout_id
    self.workout_name = workout_name
    self.workout_reps = workout_reps
    self.workout_sets = workout_sets

  def __repr__(self):
    return f'<UserWorkout {self.id} : {self.workout_name} {self.user.username}>'

  def get_json(self):
    return {
        'id': self.id,
        'name': self.workout_name,
        'reps': self.workout_reps,
        'sets': self.workout_sets
    }
