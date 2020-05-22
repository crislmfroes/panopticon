from .engine import db_engine

class User(db_engine.DynamicDocument, object):
    name = db_engine.StringField(required=True)
    email = db_engine.EmailField(required=True, unique=True)
    password = db_engine.StringField(required=True)
    tasks = db_engine.ListField(db_engine.ReferenceField('Task'))

    '''def toJSON(self):
        return {
            "name": self.name,
            "id": str(self.id)
        }'''
