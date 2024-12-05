from flask import Blueprint, jsonify, request, abort, json
from models import db, Task
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

bp = Blueprint("bp", __name__)

@bp.route('/tasks', methods=['GET'])
@jwt_required()
def all_tasks():
    #datos = get_jwt()
    #print(datos)

    # Extraemos el usuario actual del token
    current_user = json.loads(get_jwt_identity())
    print(current_user["id"])

    tasks = Task.query.filter_by(user_id=current_user["id"]) # SELECT * FROM tasks WHERE user_id = ?
    tasks = [task.serialize() for task in tasks]

    return jsonify({ "tasks": tasks}), 200

@bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
        # Extraemos el usuario actual del token
        current_user = json.loads(get_jwt_identity())

        label = request.json.get("label")
        user_id = request.json.get("user_id", current_user["id"])

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
@jwt_required()
def delete_task(id):

    task = Task.query.get(id)

    if not task:
        return jsonify({"status": "Task not found", "task": None}), 404
    
    db.session.delete(task)
    db.session.commit()

    return jsonify({"status": "Task deleted", "task": None}), 200