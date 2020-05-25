from app import app, ImageFile, db_engine, jwt, user_bp, task_bp, polygon_bp, image_bp, label_bp
from flask_mongoengine.json import override_json_encoder
import os
from flask_cors import CORS
import meinheld

meinheld.set_max_content_length(2**10 * 2**10 * 2**10 * 1) #1GB

if os.path.isfile("app/instance/config.local.cfg"):
    app.config.from_pyfile(os.path.abspath("app/instance/config.local.cfg"))
else:
    app.config.from_pyfile(os.path.abspath("app/instance/config.cfg"))
override_json_encoder(app)
db_engine.init_app(app)
jwt.init_app(app)
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)
app.register_blueprint(polygon_bp)
app.register_blueprint(image_bp)
app.register_blueprint(label_bp)
CORS(app, resources={r'/*': {'origins': '*'}})

if __name__ == '__main__':
    app.run(port=os.environ.get("PORT", 80), debug=True)
