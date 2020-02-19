import morpfw
from .schema import ReferenceDataPropertySchema



class ReferenceDataPropertyModel(morpfw.Model):
    schema = ReferenceDataPropertySchema

class ReferenceDataPropertyCollection(morpfw.Collection):
    schema = ReferenceDataPropertySchema

