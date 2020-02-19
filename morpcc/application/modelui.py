from morpcc.crud.model import CollectionUI, ModelUI


class ApplicationModelUI(ModelUI):
    pass


class ApplicationCollectionUI(CollectionUI):
    modelui_class = ApplicationModelUI

    columns = [
        {"title": "Title", "name": "title"},
        {"title": "Description", "name": "description"},
        {"title": "Actions", "name": "structure:buttons"},
    ]
