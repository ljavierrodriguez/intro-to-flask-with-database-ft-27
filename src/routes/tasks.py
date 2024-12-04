from flask import Blueprint, jsonify, request, abort
from models import db, Task

bp = Blueprint("bp", __name__)

@bp.route('/tasks', methods=['GET'])
def all_tasks():

    tasks = Task.query.all() # SELECT * FROM tasks;
    tasks = [task.serialize() for task in tasks]

    return jsonify({ "tasks": tasks}), 200

@bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        label = request.json.get("label")
        user_id = request.json.get("user_id", 1)

        if not label:
            return jsonify({"label": "this field is required"}), 400
        
        task = Task()
        task.label = label
        task.user_id = user_id

        db.session.add(task)
        db.session.commit()

        if task:
            return jsonify({ "status": "Task created", "task": task.serialize()}), 201
        else:
            return jsonify({"status": "Task not created", "task": None}), 400
        
    except Exception as e:
        print(e)
        abort(500, e)
    
@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):

    task = Task.query.get(id)

    if not task:
        return jsonify({"status": "Task not found", "task": None}), 404
    
    db.session.delete(task)
    db.session.commit()

    return jsonify({"status": "Task deleted", "task": None}), 200