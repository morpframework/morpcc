from morpcc.crud.model import ModelUI, CollectionUI


class SelectionAttributeModelUI(ModelUI):
    pass


class SelectionAttributeCollectionUI(CollectionUI):
    modelui_class = SelectionAttributeModelUI
