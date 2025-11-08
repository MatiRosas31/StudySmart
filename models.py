from flask_sqlalchemy import SQLAlchemy
from database import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.now())
    exercises = db.relationship("Exercise", backref="user", lazy=True)


class Exercise(db.Model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255))
    parts = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=db.func.now())
    result = db.relationship("ExerciseResult", backref="exercise", uselist=False)


class ExerciseResult(db.Model):
    __tablename__ = "exercise_results"
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    feedback = db.Column(db.JSON)
    overall_feedback = db.Column(db.Text)
    exercise_passed = db.Column(db.Boolean)
    score = db.Column(db.Numeric(4,2))
    created_at = db.Column(db.DateTime, default=db.func.now())

