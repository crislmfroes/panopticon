from .engine import db_engine


class Polygon(db_engine.DynamicDocument):
    points = db_engine.ListField(db_engine.FloatField())
    label = db_engine.ReferenceField('Label')

    '''def toJSON(self, label=False, image=False):
        return {
            "id": str(self.id),
            "points": self.points,
            "label": None,
            "image": None
        }'''
