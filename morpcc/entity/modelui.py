from morpcc.crud.model import CollectionUI, ModelUI


class EntityModelUI(ModelUI):
    pass


class EntityCollectionUI(CollectionUI):
    modelui_class = EntityModelUI

    columns = [
        {"title": "Table Name", "name": "name"},
        {"title": "Title", "name": "title"},
        {"title": "Actions", "name": "structure:buttons"},
    ]
