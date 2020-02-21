import morpfw
from .schema import ApplicationBehaviorAssignmentSchema


class ApplicationBehaviorAssignmentModel(morpfw.Model):
    schema = ApplicationBehaviorAssignmentSchema


class ApplicationBehaviorAssignmentCollection(morpfw.Collection):
    schema = ApplicationBehaviorAssignmentSchema
