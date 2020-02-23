from morpcc.crud.model import CollectionUI, ModelUI


class DictionaryElementModelUI(ModelUI):
    pass


class DictionaryElementCollectionUI(CollectionUI):
    modelui_class = DictionaryElementModelUI
