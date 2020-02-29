import morpfw

from .schema import EndpointSchema


class EndpointModel(morpfw.Model):
    schema = EndpointSchema


class EndpointCollection(morpfw.Collection):
    schema = EndpointSchema


class NamedEndpointModel(EndpointModel):
    @property
    def identifier(self):
        return self["name"]


class NamedEndpointCollection(EndpointCollection):
    pass
