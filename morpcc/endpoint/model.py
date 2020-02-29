import morpfw
from .schema import EndpointSchema


class EndpointModel(morpfw.Model):
    schema = EndpointSchema


class EndpointCollection(morpfw.Collection):
    schema = EndpointSchema
