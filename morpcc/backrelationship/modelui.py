from morpcc.crud.model import ModelUI, CollectionUI


class BackRelationshipModelUI(ModelUI):
    pass


class BackRelationshipCollectionUI(CollectionUI):
    modelui_class = BackRelationshipModelUI
