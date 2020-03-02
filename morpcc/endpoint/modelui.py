from morpcc.crud.model import CollectionUI, ModelUI


class EndpointModelUI(ModelUI):
    pass


class EndpointCollectionUI(CollectionUI):
    modelui_class = EndpointModelUI

    columns = [
        {"name": "name", "title": "Endpoint Name"},
        {"name": "title", "title": "Title"},
        {"name": "description", "title": "Description"},
        {"name": "structure:buttons", "title": "Actions"},
    ]
