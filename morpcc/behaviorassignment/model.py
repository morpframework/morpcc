import morpfw

#
from .modelui import BehaviorAssignmentCollectionUI, BehaviorAssignmentModelUI
from .schema import BehaviorAssignmentSchema

#


class BehaviorAssignmentModel(morpfw.Model):
    schema = BehaviorAssignmentSchema

    #
    def ui(self):
        return BehaviorAssignmentModelUI(self.request, self, self.collection.ui())


#


class BehaviorAssignmentCollection(morpfw.Collection):
    schema = BehaviorAssignmentSchema

    #

    def ui(self):
        return BehaviorAssignmentCollectionUI(self.request, self)

#

