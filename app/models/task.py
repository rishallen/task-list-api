from flask import current_app
from datetime import datetime
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)

    def to_json(self):
        if self.completed_at:
            completed = True
        else:
            completed = False

        return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "is_complete": completed,
        # "goal_id": self.goal_id # if the task belongs a goal add if not do not add
        }