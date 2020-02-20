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

        attrs = self.collection.__parent__.attributes()

        for behavior in self.collection.__parent__.behaviors():
            for n, attr in behavior.schema.__dataclass_fields__.items():
                if n in attrs.keys():
                    continue

                title = n
                if attr.metadata.get("title", None):
                    title = attr.metadata["title"]
                columns.append({"title": title, "name": n})

        for n, attr in attrs.items():
            columns.append({"title": attr["title"], "name": n})

        columns.append({"title": "Actions", "name": "structure:buttons"})

        return columns
