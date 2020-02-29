from morpcc.crud.model import ModelUI, CollectionUI


class EndpointModelUI(ModelUI):
    pass


class EndpointCollectionUI(CollectionUI):
    modelui_class = EndpointModelUI
