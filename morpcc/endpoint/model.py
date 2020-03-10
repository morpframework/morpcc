import morpfw

from .modelui import EndpointCollectionUI, EndpointModelUI
from .schema import EndpointSchema


class EndpointModel(morpfw.Model):
    schema = EndpointSchema

    def ui(self):
        return EndpointModelUI(self.request, self, self.collection.ui())


class EndpointCollection(morpfw.Collection):
    schema = EndpointSchema

    def ui(self):
        return EndpointCollectionUI(self.request, self)


class NamedEndpointModel(EndpointModel):
    @property
    def identifier(self):
        return self["name"]


class NamedEndpointCollection(EndpointCollection):
    pass
