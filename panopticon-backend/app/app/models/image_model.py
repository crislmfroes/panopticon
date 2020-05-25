from .engine import db_engine


class ImageFile(db_engine.DynamicDocument):
    name = db_engine.StringField(required=True, unique=False)
    path = db_engine.StringField(required=True, unique=True)
    polygons = db_engine.ListField(db_engine.ReferenceField('Polygon'))

    '''def toJSON(self, polygons=False, task=False):
        return {
            "id": str(self.id),
            "name": self.name,
            "path": self.path,
            "polygons": None,
            "task": None
        }'''