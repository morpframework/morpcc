from morpcc.crud.model import ModelUI, CollectionUI


class RelationshipModelUI(ModelUI):
    pass


class RelationshipCollectionUI(CollectionUI):
    modelui_class = RelationshipModelUI
