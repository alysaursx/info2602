from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Workout, UserWorkout
from sqlalchemy.exc import IntegrityError

views = Blueprint('views', __name__)

@views.route('/')
@views.route("/<int:workout_id>", methods=['GET'])
@login_required
def home(workout_id=0):
    workout_all = Workout.query.all()
    current_user_routine = current_user.routine
    selected_workout = Workout.query.get(workout_id)
    return render_template('home.html',workout_all = workout_all, current_user_routine = current_user_routine, selected_workout = selected_workout, user=current_user)

@views.route("/workout/<int:workout_id>", methods=['POST'])
@login_required
def add_workout(workout_id):
  reps = request.form['reps']
  sets = request.form['sets']
  workout = Workout.query.get(workout_id)
  routine = User.addWorkout(current_user, workout_id, workout.name, reps, sets)
  return redirect(request.referrer)

@views.route("/delworkout/<int:workout_id>", methods=['GET'])
@login_required
def del_workout(workout_id):
  workout = UserWorkout.query.get(workout_id)
  routine = User.removeWorkout(current_user, workout.id)
  return redirect(request.referrer)
  