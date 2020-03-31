import morpfw
from RestrictedPython import compile_restricted

from ..restrictedpython import get_restricted_function

#
from .modelui import EndpointHandlerCollectionUI, EndpointHandlerModelUI
from .schema import EndpointHandlerSchema

#


class EndpointHandlerModel(morpfw.Model):
    schema = EndpointHandlerSchema

    #
    def ui(self):
        return EndpointHandlerModelUI(self.request, self, self.collection.ui())

    #
    @morpfw.requestmemoize()
    def endpoint(self):
        col = self.request.get_collection("morpcc.endpoint")
        return col.get(self["endpoint_uuid"])

    @morpfw.memoize()
    def bytecode(self):
        bytecode = compile_restricted(
            self["code"],
            filename="<Endpoint Handler {} {}>".format(
                self["method"], self.endpoint()["name"]
            ),
            mode="exec",
        )
        return bytecode

    @morpfw.memoize()
    def function(self):
        function = get_restricted_function(self.request.app, self.bytecode(), "handle")
        return function


class EndpointHandlerCollection(morpfw.Collection):
    schema = EndpointHandlerSchema

    #
    def ui(self):
        return EndpointHandlerCollectionUI(self.request, self)


#
