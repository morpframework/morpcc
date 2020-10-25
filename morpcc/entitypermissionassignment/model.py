import morpfw
from .schema import EntityPermissionAssignmentSchema
# 
from .modelui import EntityPermissionAssignmentModelUI, EntityPermissionAssignmentCollectionUI
# 

class EntityPermissionAssignmentModel(morpfw.Model):
    schema = EntityPermissionAssignmentSchema

# 
    def ui(self):
        return EntityPermissionAssignmentModelUI(self.request, self,
                self.collection.ui())
# 


class EntityPermissionAssignmentCollection(morpfw.Collection):
    schema = EntityPermissionAssignmentSchema

# 
    def ui(self):
        return EntityPermissionAssignmentCollectionUI(self.request, self)
# 

