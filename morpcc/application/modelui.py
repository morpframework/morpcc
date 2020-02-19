from morpcc.crud.model import ModelUI, CollectionUI


class ApplicationModelUI(ModelUI):
    pass


class ApplicationCollectionUI(CollectionUI):
    modelui_class = ApplicationModelUI
