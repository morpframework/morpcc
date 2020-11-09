import morpfw
from .schema import EntityContentIndexQueueSchema
# 
from .modelui import EntityContentIndexQueueModelUI, EntityContentIndexQueueCollectionUI
# 

class EntityContentIndexQueueModel(morpfw.Model):
    schema = EntityContentIndexQueueSchema

# 
    def ui(self):
        return EntityContentIndexQueueModelUI(self.request, self,
                self.collection.ui())
# 


class EntityContentIndexQueueCollection(morpfw.Collection):
    schema = EntityContentIndexQueueSchema

# 
    def ui(self):
        return EntityContentIndexQueueCollectionUI(self.request, self)
# 

