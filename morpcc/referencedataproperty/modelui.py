from morpcc.crud.model import ModelUI, CollectionUI


class ReferenceDataPropertyModelUI(ModelUI):
    pass


class ReferenceDataPropertyCollectionUI(CollectionUI):
    modelui_class = ReferenceDataPropertyModelUI
