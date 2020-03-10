import morpfw

from .schema import EntityValidatorAssignmentSchema


class EntityValidatorAssignmentModel(morpfw.Model):
    schema = EntityValidatorAssignmentSchema

    def validator(self):
        col = self.request.get_collection("morpcc.entityvalidator")
        return col.get(self["entityvalidator_uuid"])

    def entity(self):
        col = self.request.get_collection("morpcc.entity")
        return col.get(self["entity_uuid"])


class EntityValidatorAssignmentCollection(morpfw.Collection):
    schema = EntityValidatorAssignmentSchema
