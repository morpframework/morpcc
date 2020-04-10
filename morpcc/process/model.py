import morpfw
from .schema import ProcessSchema
# 
from .modelui import ProcessModelUI, ProcessCollectionUI
# 

class ProcessModel(morpfw.Model):
    schema = ProcessSchema

# 
    def ui(self):
        return ProcessModelUI(self.request, self,
                self.collection.ui())
# 


class ProcessCollection(morpfw.Collection):
    schema = ProcessSchema

# 
    def ui(self):
        return ProcessCollectionUI(self.request, self)
# 

