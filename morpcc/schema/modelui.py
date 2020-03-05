from morpcc.crud.model import ModelUI, CollectionUI


class SchemaModelUI(ModelUI):
    pass


class SchemaCollectionUI(CollectionUI):
    modelui_class = SchemaModelUI
