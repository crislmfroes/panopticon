from flask import Blueprint, abort, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Polygon, User, ImageFile, Label, Task
from flask_mongoengine.json import json_util


label_bp = Blueprint('label_bp', __name__, url_prefix='/labels')

@label_bp.route('/add', methods=["POST"])
@jwt_required
def add(label_dict=None, raw=False):
    content = label_dict if label_dict else request.json
    user_id = label_dict["user_id"] if label_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task in user.tasks:
        label = Label()
        label.color = content["color"]
        label.name = content["name"]
        label.isthing = content["isthing"]
        label.save()
        task.labels.append(label)
        task.save()
        return (label.to_json(), 200) if not raw else label
    abort(404)


@label_bp.route('/update', methods=["POST"])
@jwt_required
def update(label_dict=None, raw=False):
    content = label_dict if label_dict else request.json
    user_id = label_dict["user_id"] if label_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task in user.tasks:
        label = Label.objects(id=content["id"]).first()
        if label and label in task.labels:
            color = content.get("color", None)
            name = content.get("name", None)
            isthing = content.get("isthing", None)
            label.color = color if color is not None else label.color
            label.name = name if name is not None else label.name
            label.isthing = isthing if isthing is not None else label.isthing
            label.save()
            return (label.to_json(), 200) if not raw else label
    abort(404)


@label_bp.route('/list', methods=["GET"])
@jwt_required
def list_labels(label_dict=None, raw=False):
    response = []
    content = label_dict if label_dict else request.json
    user_id = label_dict["user_id"] if label_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task in user.tasks:
        for label in task.labels:
            response.append(label.to_mongo())
        return (json_util.dumps(response), 200) if not raw else task.labels
    abort(404)


@label_bp.route('/delete', methods=["GET"])
@jwt_required
def delete(label_dict=None, raw=False):
    content = label_dict if label_dict else request.json
    user_id = label_dict["user_id"] if label_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task in user.tasks:
        label = Label.objects(id=content["id"]).first()
        if label and label in task.labels:
            label.delete()
            task.save()
            return (jsonify(), 200) if not raw else None
    abort(404)


@task_bp.route('/save', methods=["POST"])
@jwt_required
def save(task_dict=None, raw=False):
    response = []
    content = task_dict.copy() if task_dict else request.json.copy()
    user_id = task_dict["user_id"] if task_dict else get_jwt_identity()
    content["user_id"] = user_id
    if 'id' in content:
        return add(label_dict=content, raw=raw)
    else:
        return update(label_dict=content, raw=raw)
