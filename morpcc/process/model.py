import morpfw

#
from .modelui import ProcessCollectionUI, ProcessModelUI
from .schema import ProcessSchema

#


class ProcessModel(morpfw.Model):
    schema = ProcessSchema

    blob_fields = ["output"]
    #
    def ui(self):
        return ProcessModelUI(self.request, self, self.collection.ui())


#


class ProcessCollection(morpfw.Collection):
    schema = ProcessSchema

    #
    def ui(self):
        return ProcessCollectionUI(self.request, self)

#

