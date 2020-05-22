from .engine import db_engine

class Task(db_engine.DynamicDocument):
    name = db_engine.StringField(required=True)
    user = db_engine.ReferenceField('User')
    labels = db_engine.ListField(db_engine.ReferenceField('Label'))
    images = db_engine.ListField(db_engine.ReferenceField('ImageFile'))

    '''def toJSON(self, user=False, labels=False, images=False):
        return {
            "id": str(self.id),
            "name": self.name,
            "user": self.user.toJSON() if user else None
        }'''