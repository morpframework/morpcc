import morpfw

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

    def validator(self):
        col = self.request.get_collection("morpcc.entityvalidator")
        return col.get(self["entityvalidator_uuid"])

    def entity(self):
        col = self.request.get_collection("morpcc.entity")
        return col.get(self["entity_uuid"])


class EntityValidatorAssignmentCollection(morpfw.Collection):
    schema = EntityValidatorAssignmentSchema

    def ui(self):
        return EntityValidatorAssignmentCollectionUI(self.request, self)
