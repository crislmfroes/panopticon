from app import app, db_engine, jwt, user_bp, task_bp, polygon_bp, image_bp, label_bp
from flask_mongoengine.json import override_json_encoder
import os

if __name__ =='__main__':
    if os.path.isfile("instance/config.cfg"):
        app.config.from_pyfile(os.path.abspath("instance/config.cfg"))
    elif os.path.isfile("instance/config.local.cfg"):
        app.config.from_pyfile(os.path.abspath("instance/config.local.cfg"))
    app.config["MONGODB_SETTINGS"]["db"] = os.environ.get("MONGODB_DB") if os.environ.get("MONGODB_DB", None) else app.config["MONGODB_SETTINGS"]["db"]
    app.config["MONGODB_SETTINGS"]["host"] = os.environ.get("MONGODB_HOST") if os.environ.get("MONGODB_HOST", None) else app.config["MONGODB_SETTINGS"]["host"]
    app.config["MONGODB_SETTINGS"]["port"] = os.environ.get("MONGODB_PORT") if os.environ.get("MONGODB_PORT", None) else app.config["MONGODB_SETTINGS"]["port"]
    override_json_encoder(app)
    db_engine.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(polygon_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(label_bp)
    app.run()