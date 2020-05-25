from flask import Blueprint, request, Response, abort, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User, Task, Label
from flask_mongoengine.json import json_util
import os
from zipfile import ZipFile
from .image_bp import save as save_image
from .label_bp import save as save_label

task_bp = Blueprint('task_bp', __name__, url_prefix='/api/tasks')


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
        user.tasks.remove(task)
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
    content = task_dict.copy() if task_dict else request.json.copy()
    user_id = task_dict["user_id"] if task_dict else get_jwt_identity()
    content["user_id"] = user_id
    if 'id' in content:
        return update(task_dict=content, raw=raw)
    else:
        return add(task_dict=content, raw=raw)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ("zip",)

def allowed_unzip_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ("jpg",)


@task_bp.route('/upload', methods=["POST"])
@jwt_required
def upload(task_dict=None, raw=False):
    content = task_dict if task_dict else request.json
    user_id = task_dict["user_id"] if task_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["id"]).first()
    files = task_dict["files"] if task_dict else request.files
    if 'file' in files:
        file = files["file"]
        if file and file.filename and allowed_file(file.filename) and task in user.tasks:
            filename = secure_filename(file.filename)
            os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id), str(content["id"])), exist_ok=True)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id), str(content["id"]), filename))
            paths = []
            with ZipFile(os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id), str(content["id"]), filename), 'r') as zip_ref:
                zip_ref.extractall(os.path.join(
                    current_app.config['UPLOAD_FOLDER'], str(user_id), str(content["id"])))
                for dirpath, dirnames, filenames in os.walk(os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id), str(content["id"]))):
                    for unzip_filename in filenames:
                        if allowed_unzip_file(unzip_filename):
                            paths.append(os.path.join(dirpath, unzip_filename))
            return (jsonify(paths), 200) if not raw else paths
    abort(404)


@task_bp.route('/create', methods=["POST"])
@jwt_required
def create():
    content = request.form
    user_id = get_jwt_identity()
    task = save(task_dict={
        "user_id": user_id,
        "name": content["name"]
    }, raw=True)
    paths = upload(task_dict={
        "user_id": user_id,
        "id": task.id,
        "files": request.files
    }, raw=True)
    for path in paths:
        save_image(image_dict={
            "user_id": user_id,
            "task_id": task.id,
            "path": path,
            "name": os.path.basename(path)
        }, raw=True)
    for labelname, color, isthing in zip(content.getlist("label"), content.getlist("color"), content.getlist("isthing")):
        color = int(color)
        if isthing == 'true':
            isthing = True
        elif isthing == 'false':
            isthing = False
        else:
            abort(500)
        save_label(label_dict={
            "user_id": user_id,
            "task_id": task.id,
            "name": labelname,
            "color": color,
            "isthing": isthing
        }, raw=True)
    return Response(status=200)
