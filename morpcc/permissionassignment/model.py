import morpfw
import rulez

# 
from .modelui import (PermissionAssignmentCollectionUI,
                      PermissionAssignmentModelUI)
from .schema import PermissionAssignmentSchema

# 

class PermissionAssignmentModel(morpfw.Model):
    schema = PermissionAssignmentSchema

# 
    def ui(self):
        return PermissionAssignmentModelUI(self.request, self,
                self.collection.ui())
# 


class PermissionAssignmentCollection(morpfw.Collection):
    schema = PermissionAssignmentSchema

# 
    def ui(self):
        return PermissionAssignmentCollectionUI(self.request, self)
# 

    @morpfw.requestmemoize()
    def lookup_permission(self, model_name, permission_name, enabled):
        return self.search(
            rulez.and_(
                rulez.field["model"] == model_name,
                rulez.field["permission"] == permission_name,
                rulez.field["enabled"] == True,
            )
        )
