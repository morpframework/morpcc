from morpcc.crud.model import CollectionUI, ModelUI


class EntityContentModelUI(ModelUI):
    pass


class EntityContentCollectionUI(CollectionUI):
    modelui_class = EntityContentModelUI

    @property
    def columns(self):
        columns = []

        attrs = self.collection.__parent__.effective_attributes()
        rels = self.collection.__parent__.relationships()
        for n, attr in attrs.items():
            columns.append({"title": attr["title"], "name": n})

        for n, rel in rels.items():
            columns.append({"title": rel["title"], "name": n})

        columns.append({"title": "Actions", "name": "structure:buttons"})

        return columns
