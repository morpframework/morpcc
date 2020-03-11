from morpcc.crud.model import ModelUI, CollectionUI


class EndpointHandlerModelUI(ModelUI):
    pass


class EndpointHandlerCollectionUI(CollectionUI):
    modelui_class = EndpointHandlerModelUI
