import morpfw

from .schema import SelectionAttributeSchema


class SelectionAttributeModel(morpfw.Model):
    schema = SelectionAttributeSchema

    def datatype(self):
        return str

    def entity(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.entity", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        dm = col.get(self["entity_uuid"])
        return dm


class SelectionAttributeCollection(morpfw.Collection):
    schema = SelectionAttributeSchema
