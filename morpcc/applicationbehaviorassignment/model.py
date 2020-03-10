import morpfw

from .modelui import (
    ApplicationBehaviorAssignmentCollectionUI,
    ApplicationBehaviorAssignmentModelUI,
)
from .schema import ApplicationBehaviorAssignmentSchema


class ApplicationBehaviorAssignmentModel(morpfw.Model):
    schema = ApplicationBehaviorAssignmentSchema

    def ui(self):
        return ApplicationBehaviorAssignmentModelUI(
            self.request, self, self.collection.ui()
        )


class ApplicationBehaviorAssignmentCollection(morpfw.Collection):
    schema = ApplicationBehaviorAssignmentSchema

    def ui(self):
        return ApplicationBehaviorAssignmentCollectionUI(self.request, self)
