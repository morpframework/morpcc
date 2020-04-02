import morpfw
import rulez

from .modelui import (
    EntityValidatorAssignmentCollectionUI,
    EntityValidatorAssignmentModelUI,
)
from .schema import EntityValidatorAssignmentSchema


class EntityValidatorAssignmentModel(morpfw.Model):
    schema = EntityValidatorAssignmentSchema

    def ui(self):
        return EntityValidatorAssignmentModelUI(
            self.request, self, self.collection.ui()
        )

    @morpfw.requestmemoize()
    def validator(self):
        col = self.request.get_collection("morpcc.entityvalidator")
        validators = col.search(rulez.field["name"] == self["entityvalidator_name"])
        if validators:
            return validators[0]
        return None

    @morpfw.requestmemoize()
    def entity(self):
        col = self.request.get_collection("morpcc.entity")
        return col.get(self["entity_uuid"])


class EntityValidatorAssignmentCollection(morpfw.Collection):
    schema = EntityValidatorAssignmentSchema

    def ui(self):
        return EntityValidatorAssignmentCollectionUI(self.request, self)
