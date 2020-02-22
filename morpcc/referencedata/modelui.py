from morpcc.crud.model import ModelUI, CollectionUI


class ReferenceEntityUI(ModelUI):
    pass


class ReferenceDataCollectionUI(CollectionUI):
    modelui_class = ReferenceEntityUI

    columns = [
        {"title": "Title", "name": "title"},
        {"title": "Identifier Name", "name": "name"},
        {"title": "Actions", "name": "structure:buttons"},
    ]

