from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Workout, UserWorkout

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
  # implement save newly captured pokemon, show a message then reload page
  reps = request.form['reps']
  sets = request.form['sets']
  workout = Workout.query.get(workout_id)
  User.addWorkout(current_user, workout_id, workout.name, reps, sets)
  return redirect(request.referrer)