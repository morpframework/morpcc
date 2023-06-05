from ..app import App
from .model import CollectionUI, ModelUI
from morpfw.crud.metalink import MetalinkProvider

class CollectionUIMetalinkProvider(MetalinkProvider):
    def link(self, obj, view_name=None, **kwargs) -> dict:
        typeinfo = self.app.get_typeinfo_by_schema(obj.schema, self.request)
        return {
            "type": "morpcc.collectionui",
            "resource_type": typeinfo["name"],
            "view_name": view_name,
        }

    def resolve(self, link) -> str:
        col = self.request.get_collection(link["resource_type"])
        return self.request.link(col.ui())


class ModelUIMetalinkProvider(MetalinkProvider):
    def link(self, obj, view_name=None, **kwargs) -> dict:
        typeinfo = self.app.get_typeinfo_by_schema(obj.schema, self.request)
        return {
            "type": "morpcc.modelui",
            "resource_type": typeinfo["name"],
            "uuid": obj.uuid,
            "view_name": view_name,
        }

    def resolve(self, link) -> str:
        col = self.request.get_collection(link["resource_type"])
        return self.request.link(col.get_by_uuid(link["uuid"]).ui())


@App.metalink(name="morpcc.collectionui", model=CollectionUI)
def get_collection_metalink(request):
    return CollectionUIMetalinkProvider(request)


@App.metalink(name="morpcc.modelui", model=ModelUI)
def get_model_metalink(request):
    return ModelUIMetalinkProvider(request)

