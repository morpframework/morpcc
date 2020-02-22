from morpcc.crud.model import ModelUI, CollectionUI


class EntityConstraintModelUI(ModelUI):
    pass


class EntityConstraintCollectionUI(CollectionUI):
    modelui_class = EntityConstraintModelUI
