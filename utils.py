from models import User, Exercise, ExerciseResult
from database import db

def user_check(data):
    user = User.query.filter_by(username=data.get("username")).first()
    if not user:
        user = User(username=data.get("username", "anon"))
        db.session.add(user)
        db.session.commit()
    return user

def Save_excercise(user, data):
    exercise = Exercise(user_id=user.id, title=data.get("title"), parts=data["parts"])
    db.session.add(exercise)
    db.session.commit() 
    return exercise 

def Save_result(exercise, parsed_json):
    result = ExerciseResult(
        exercise_id=exercise.id,
        feedback=parsed_json.get("feedback"),
        overall_feedback=parsed_json.get("overall_feedback"),
        exercise_passed=parsed_json.get("exercise_passed"),
        score=parsed_json.get("feedback")[0].get("score") if parsed_json.get("feedback") else None
    )
    db.session.add(result)
    db.session.commit()