from morpcc.crud.model import CollectionUI, ModelUI


class ReferenceDataModelUI(ModelUI):
    pass


class ReferenceDataCollectionUI(CollectionUI):
    modelui_class = ReferenceDataModelUI

    columns = [
        {"title": "Title", "name": "title"},
        {"title": "Identifier Name", "name": "name"},
        {"title": "Actions", "name": "structure:buttons"},
    ]
