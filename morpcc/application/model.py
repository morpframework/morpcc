import warnings
from dataclasses import field, make_dataclass

import morpfw
import rulez
from morpfw.crud import signals
from morpfw.crud.storage.pgsqlstorage import PgSQLStorage
from sqlalchemy import DDL, MetaData

from ..entitycontent.path import content_collection_factory
from ..index.model import IndexContentCollection, IndexContentModel
from .modelui import (
    ApplicationCollectionUI,
    ApplicationModelUI,
    BehaviorableApplicationModelUI,
)
from .schema import ApplicationSchema


def get_behaviors(request, app_uuid):
    col = request.get_collection("morpcc.applicationbehaviorassignment")
    assignments = col.search(rulez.field["application_uuid"] == app_uuid)
    behaviors = []
    for assignment in assignments:
        behavior = request.app.config.application_behavior_registry.get_behavior(
            assignment["behavior"], request
        )
        behaviors.append(behavior)
    return behaviors


class ApplicationModel(morpfw.Model):
    schema = ApplicationSchema

    def ui(self):
        return BehaviorableApplicationModelUI(self.request, self, self.collection.ui())

    def title(self):
        return self["title"]

    @morpfw.requestmemoize()
    def application_schema(self):
        col = self.request.get_collection("morpcc.schema")
        return col.get(self["schema_uuid"])

    @morpfw.requestmemoize()
    def entities(self):
        return self.application_schema().entities()

    @morpfw.requestmemoize()
    def entity_collections(self):
        result = {}
        for entity in self.application_schema().entities():
            result[entity["name"]] = content_collection_factory(entity, self)
        return result

    def content_metadata(self):
        return MetaData(schema=self["name"])

    @morpfw.requestmemoize()
    def behaviors(self):
        return get_behaviors(self.request, self.uuid)

    def reindex(self):
        for dm in self.entities():
            col = dm.content_collection()
            agg = col.aggregate(group={"total": {"function": "count", "field": "*"}})
            total = agg["total"]
            offset = 0
            while True:
                dms = dm.search(offset=offset, limit=1000, secure=False)
                if len(dms) == 0:
                    break

                for dmc in dms:
                    self.index_sync(dmc)
                    count += 1

                offset += 1000

    def index_sync(self, model):
        col = self.request.get_collection("morpcc.index")
        idxcol = col.content_collection()
        return idxcol.index(model)

    def unindex(self, model):
        col = self.request.get_collection("morpcc.index")
        idxcol = col.content_collection()
        idxcol.unindex(model)

    def drop_all(self):
        for ec in self.entity_collections().values():
            ec.drop_all()

    def before_delete(self):
        sm = self.statemachine()
        sm.delete()
        self.request.async_dispatch("morpcc.delete_application")
        return False


class BehaviorableApplicationModel(ApplicationModel):
    def __new__(cls, request, collection, data):
        prov = request.app.get_dataprovider(cls.schema, data, collection.storage)

        behaviors = get_behaviors(request, prov["uuid"])
        if not behaviors:
            return ApplicationModel(request, collection, data)

        markers = [behavior.model_marker for behavior in behaviors]
        markers.append(ApplicationModel)
        klass = type(
            "ApplicationModel", tuple(markers), {"__path_model__": ApplicationModel}
        )
        return klass(request, collection, data)


class ApplicationCollection(morpfw.Collection):
    schema = ApplicationSchema

    def ui(self):
        return ApplicationCollectionUI(self.request, self)

    def get_by_name(self, name):
        results = self.search(rulez.field["name"] == name)
        if results:
            return results[0]
        return None

    def search(self, query=None, offset=0, limit=None, order_by=None, secure=False):
        if query is None:
            warnings.warn(
                "Searching application does not exclude ones that are pending deletion."
                "Recommended to use .all() to list all applications",
                stacklevel=2,
            )
        return super().search(query, offset, limit, order_by, secure)

    @morpfw.requestmemoize()
    def all(self):
        """
        Return all applications, excluding ones that are being deleted
        """
        return self.search(
            rulez.or_(
                rulez.field("state") == None,
                rulez.and_(
                    rulez.field("state") != "process_delete",
                    rulez.field("state") != "deleting",
                ),
            )
        )
