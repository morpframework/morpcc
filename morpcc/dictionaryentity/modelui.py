from morpcc.crud.model import ModelUI, CollectionUI


class DictionaryEntityModelUI(ModelUI):
    pass


class DictionaryEntityCollectionUI(CollectionUI):
    modelui_class = DictionaryEntityModelUI
