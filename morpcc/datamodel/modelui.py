from morpcc.crud.model import CollectionUI, ModelUI


class DataModelModelUI(ModelUI):
    pass


class DataModelCollectionUI(CollectionUI):
    modelui_class = DataModelModelUI

    columns = [
        {"title": "Table Name", "name": "name"},
        {"title": "Title", "name": "title"},
        {"title": "Actions", "name": "structure:buttons"},
    ]


class DataModelContentModelUI(ModelUI):
    pass


class DataModelContentCollectionUI(CollectionUI):
    modelui_class = DataModelContentModelUI

    @property
    def columns(self):
        columns = []

        for n, attr in self.collection.__parent__.attributes().items():
            columns.append({"title": attr["title"], "name": n})
        columns.append({"title": "Actions", "name": "structure:buttons"})

        return columns
