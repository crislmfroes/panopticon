from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Polygon, User, ImageFile, Label
from flask_mongoengine.json import json_util

polygon_bp = Blueprint('polygon_bp', __name__, url_prefix='/api/polygons')


@polygon_bp.route('/add', methods=["POST"])
@jwt_required
def add(polygon_dict=None, raw=False):
    content = polygon_dict if polygon_dict else request.json
    user_id = polygon_dict["user_id"] if polygon_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task and task in user.tasks:
        image = ImageFile.objects(id=content["image_id"]).first()
        if image and image in task.images:
            label = Labels.objects(id=content["label_id"]).first()
            if label and label in image.labels:
                polygon = Polygon()
                polygon.points = content["points"]
                polygon.label = label
                polygon.save()
                image.polygons.append(polygon)
                image.save()
                return (polygon.to_json(), 200) if not raw else polygon
            abort(404)
    abort(403)


@polygon_bp.route('/update', methods=["POST"])
@jwt_required
def update(polygon_dict=None, raw=False):
    content = polygon_dict if polygon_dict else request.json
    user_id = polygon_dict["user_id"] if polygon_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task and task in user.tasks:
        image = ImageFile.objects(id=content["image_id"]).first()
        if image and image in task.images:
            polygon = Polygon.objects(id=content["id"]).first()
            label = Labels.objects(id=content["label_id"]).first() if 'label_id' in content else None
            if polygon and polygon in image.polygons:
                points = content.get("points", None)
                polygon.points = points if points else polygon.points
                if label and label in image.labels:
                    polygon.label = label
                polygon.save()
                return (polygon.to_json(), 200) if not raw else polygon
            abort(404)
    abort(403)


@polygon_bp.route('/delete', methods=["POST"])
@jwt_required
def delete(polygon_dict=None, raw=False):
    content = polygon_dict if polygon_dict else request.json
    user_id = polygon_dict["user_id"] if polygon_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task and task in user.tasks:
        image = ImageFile.objects(id=content["image_id"]).first()
        if image and image in task.images:
            polygon = Polygon.objects(id=content["id"]).first()
            if polygon and polygon in image.polygons:
                image.polygons.remove(polygon)
                image.save()
                return (jsonify(), 200) if not raw else None
            abort(404)
    abort(403)


@polygon_bp.route('/list', methods=["POST"])
@jwt_required
def list_polygons(polygon_dict=None, raw=False):
    response = []
    content = polygon_dict if polygon_dict else request.json
    user_id = polygon_dict["user_id"] if polygon_dict else get_jwt_identity()
    user = User.objects(id=user_id).first()
    task = Task.objects(id=content["task_id"]).first()
    if task and task in user.tasks:
        image = ImageFile.objects(id=content["image_id"]).first()
        if image and image in task.images:
            for polygon in image.polygons:
                response.append(polygon.to_mongo())
            return (json_util.dumps(response), 200) if not raw else image.polygons
    abort(403)


@polygon_bp.route('/save', methods=["POST"])
@jwt_required
def save(polygon_dict=None, raw=False):
    response = []
    content = polygon_dict.copy() if polygon_dict else request.json.copy()
    user_id = polygon_dict["user_id"] if polygon_dict else get_jwt_identity()
    content["user_id"] = user_id
    if 'id' in content:
        return update(polygon_dict=content, raw=raw)
    else:
        return add(polygon_dict=content, raw=raw)
