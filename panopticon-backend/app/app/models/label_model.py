from .engine import db_engine

class Label(db_engine.DynamicDocument):
    name = db_engine.StringField(required=True)
    isthing = db_engine.BooleanField(default=False)
    color = db_engine.IntField(min_value=0, default=0xFF00FF)
