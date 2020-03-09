from morpcc.crud.model import ModelUI, CollectionUI


class EntityValidatorModelUI(ModelUI):
    pass


class EntityValidatorCollectionUI(CollectionUI):
    modelui_class = EntityValidatorModelUI
