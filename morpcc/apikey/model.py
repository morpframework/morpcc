from ..crud.model import CollectionUI, ModelUI


class APIKeyModelUI(ModelUI):
    pass


class APIKeyCollectionUI(CollectionUI):

    modelui_class = APIKeyModelUI
    create_view_enabled = True

    columns = [
        {"title": "Name", "name": "name"},
        {"title": "Identity", "name": "api_identity"},
        {"title": "Actions", "name": "structure:buttons"},
    ]
