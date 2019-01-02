from ..morpcc.crud.model import ModelUI, CollectionUI


class DataAssetModelUI(ModelUI):
    pass


class DataAssetCollectionUI(CollectionUI):
    modelui_class = DataAssetModelUI
