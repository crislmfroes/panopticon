from flask import Blueprint, request, Response, abort, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User, Task, Label
from flask_mongoengine.json import json_util
import os
from zipfile import ZipFile

task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')


@task_bp.route('/add', methods=["POST"])
@jwt_required
def add(task_dict=None, raw=False):
    content = task_dict if task_dict else request.json
    user_id = task_dict["user_id"] if task_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task()
    task.name = content["name"]
    task.save()
    user.tasks.append(task)
    user.save()
    return (task.to_json(), 200) if not raw else task


@task_bp.route('/delete', methods=["POST"])
@jwt_required
def delete(task_dict=None, raw=False):
    content = task_dict if task_dict else request.json
    user_id = task_dict["user_id"] if task_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["id"]).first()
    if task and task in user.tasks:
        task.delete()
        user.save()
        return Response(status=200) if not raw else None
    abort(404)


@task_bp.route('/update', methods=["POST"])
@jwt_required
def update(task_dict=None, raw=False):
    content = task_dict if task_dict else request.json
    user_id = task_dict["user_id"] if task_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["id"]).first()
    if task and task in user.tasks:
        name = content.get("name", None)
        task.name = name if name else task.name
        task.save()
        return task.to_json() if not raw else task
    abort(404)


@task_bp.route('/list', methods=["GET"])
@jwt_required
def task_list(task_dict=None, raw=False):
    response = []
    user_id = task_dict["user_id"] if task_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    tasks = user.tasks
    for task in tasks:
        response.append(task.to_mongo())
    return (json_util.dumps(response), 200) if not raw else tasks


@task_bp.route('/save', methods=["POST"])
@jwt_required
def save(task_dict=None, raw=False):
    response = []
    content = task_dict.copy() if task_dict else request.json.copy()
    user_id = task_dict["user_id"] if task_dict else get_jwt_identity()
    content["user_id"] = user_id
    if 'id' in content:
        return add(task_dict=content, raw=raw)
    else:
        return update(task_dict=content, raw=raw)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ("zip",)


@task_bp.route('/upload', methods=["POST"])
@jwt_required
def upload(task_dict=None, raw=False):
    content = task_dict if task_dict else request.json
    user_id = task_dict["user_id"] if task_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["id"]).first()
    if 'file' in request.files:
        file = request.files["file"]
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], user_id, content["id"]), exist_ok=True)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], user_id, content["id"], filename))
            paths = []
            with ZipFile(os.path.join(current_app.config['UPLOAD_FOLDER'], user_id, content["id"]), 'r') as zip_ref:
                zip_ref.extractall(os.path.join(current_app.config['UPLOAD_FOLDER'], user_id, content["id"])
                for dirpath, dirnames, filenames in os.walk(os.path.join(current_app.config['UPLOAD_FOLDER'], user_id, content["id"]):
                    paths.append(os.path.join(dirpath, dirname))
            return (jsonify(paths), 200) if not raw else paths
    abort(404)
