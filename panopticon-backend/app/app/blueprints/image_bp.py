from flask import Blueprint, abort, request, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Polygon, User, ImageFile, Label, Task
from flask_mongoengine.json import json_util
import os


image_bp = Blueprint('image_bp', __name__, url_prefix='/api/images')


@image_bp.route('/get', methods=["POST"])
@jwt_required
def get(image_dict=None, raw=False):
    content = image_dict if image_dict else request.json
    user_id = image_dict["user_id"] if image_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task in user.tasks:
        image = ImageFile.objects(id=content["id"]).first()
        if image in task.images:
            return (image.to_json(), 200) if not raw else image
    abort(404)


@image_bp.route('/add', methods=["POST"])
@jwt_required
def add(image_dict=None, raw=False):
    content = image_dict if image_dict else request.json
    user_id = image_dict["user_id"] if image_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task in user.tasks:
        image = ImageFile()
        image.name = content["name"]
        image.path = content["path"]
        image.save()
        task.images.append(image)
        task.save()
        return (image.to_json(), 200) if not raw else image
    abort(404)


@image_bp.route('/update', methods=["POST"])
@jwt_required
def update(image_dict=None, raw=False):
    content = image_dict if image_dict else request.json
    user_id = image_dict["user_id"] if image_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task in user.tasks:
        image = ImageFile.objects(id=content["id"]).first()
        if image and image in task.images:
            name = content.get("name", None)
            path = content.get("path", None)
            image.name = name if name else image.name
            image.path = path if path else image.path
            image.save()
            return (image.to_json(), 200) if not raw else image
    abort(404)


@image_bp.route('/delete', methods=["POST"])
@jwt_required
def delete(image_dict=None, raw=False):
    content = image_dict if image_dict else request.json
    user_id = image_dict["user_id"] if image_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task in user.tasks:
        image = ImageFile.objects(id=content["id"]).first()
        if image and image in task.images:
            task.images.remove(image)
            task.save()
            return (jsonify(), 200) if not raw else None
    abort(404)


@image_bp.route('/list', methods=["GET"])
@jwt_required
def list_images(image_dict=None, raw=False):
    response = []
    content = image_dict if image_dict else request.json
    user_id = image_dict["user_id"] if image_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task in user.tasks:
        for image in task.images:
            response.append(image.to_mongo())
        return (json_util.dumps(response), 200) if not raw else task.images
    abort(404)


@image_bp.route('/save', methods=["POST"])
@jwt_required
def save(image_dict=None, raw=False):
    response = []
    content = image_dict.copy() if image_dict else request.json.copy()
    user_id = image_dict["user_id"] if image_dict else get_jwt_identity()
    content["user_id"] = user_id
    if 'id' in content:
        return update(image_dict=content, raw=raw)
    else:
        return add(image_dict=content, raw=raw)
