from morpcc.crud.model import ModelUI, CollectionUI


class AttributeModelUI(ModelUI):
    pass


class AttributeCollectionUI(CollectionUI):
    modelui_class = AttributeModelUI
