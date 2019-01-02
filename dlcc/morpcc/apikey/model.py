from ..crud.model import ModelUI, CollectionUI


class APIKeyModelUI(ModelUI):
    pass


class APIKeyCollectionUI(CollectionUI):

    modelui_class = APIKeyModelUI

    columns = [
        {'title': 'Label', 'name': 'label'},
        {'title': 'Identity', 'name': 'api_identity'},
        {'title': 'Actions', 'name': 'structure:buttons'}
    ]
