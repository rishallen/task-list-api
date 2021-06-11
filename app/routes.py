from app import db
from flask import Blueprint, json
from sqlalchemy import asc, desc 
from app.models.task import Task
from datetime import datetime
from sqlalchemy.sql.functions import now
from flask import request, make_response, jsonify


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# return all tasks
@task_bp.route("/", methods=["GET", "POST"], strict_slashes = False)
def handle_tasks():
    if request.method == "GET":

        # tasks by asc and desc order
        sort_by_url = request.args.get("sort") # query parameters and replace the previous query
        if sort_by_url == "asc": # this is a list queried by title in asc order
            tasks = Task.query.order_by(Task.title.asc()).all() 
        elif sort_by_url == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all() 
        else:
            tasks = Task.query.all()
        # end of the new code
    
        tasks_response = []
        for task in tasks:
            if task.completed_at == None:
                completed_at = False
            else:
                task.completed_at = True
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": completed_at,
            })
        return make_response(jsonify(tasks_response), 200)


#create a task with null completed at
    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return {"details": "Invalid data"}, 400
            
        if not "completed_at" in request_body or not request_body["completed_at"]:
            completed_at = False
        else:
            completed_at = True
        
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"], 
            completed_at=request_body["completed_at"]
        )

        db.session.add(new_task) # "adds model to the db"
        db.session.commit() # commits the action above

        return make_response({
            "task":{ 
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": completed_at
            }
        }), 201   

# return one task
@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes = False)
def handle_task(task_id):
    task = Task.query.get(task_id)

    if request.method == "GET":
        if task is None:
            return make_response(f"Task #{task_id} not found"), 404
        if not task.completed_at:
            completed_at = False
        else:
            completed_at = task.completed_at["completed_at"]
        return {
            "task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": completed_at
            }
        }, 200

    # Update a task
    elif request.method == "PUT":
        if task is None:
            return make_response(f"Task #{task_id} not found"), 404
        form_data = request.get_json()

        if "title" not in form_data or "description" not in form_data or "completed_at" not in form_data:
            return {"details": "Invalid data"}, 400

        if not "completed_at" in form_data or not form_data["completed_at"]:
            is_complete = False
        else:
            is_complete = True            
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]

        db.session.commit()
        return {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description, 
                "is_complete": is_complete
            }
        }, 200

    # Delete a task
    elif request.method == "DELETE":
        if not task:
            return "", 404
        db.session.delete(task)
        db.session.commit()
        return {
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
        }, 200
            

# modify complete task
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes = False)
def mark_task_complete(task_id):
    task = Task.query.get(task_id)

    if not task: # this is the task check (wash my car)
        return make_response(f"Task #{task_id} not found"), 404
    task.completed_at = datetime.utcnow()
    db.session.commit()

    response_body = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True # this is always true bc we are always setting completed at
        }
    }
    return jsonify(response_body), 200

# # modify incomplete task 
# @task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def make_task_incomplete(task_id):
#     task = Task.query.get(task_id)

#     if task is None:
#         return make_response(f"Task #{task_id} not found"), 404
#     else:
#         task.completed_at = None
#         db.session.commit()
#     response_body = {
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": task.completed_at
#         }
#     }
#     return jsonify(response_body), 200
