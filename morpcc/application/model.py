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
        existing = idxcol.search(
            rulez.and_(
                rulez.field["application_uuid"]
                == model.collection.__application__.uuid,
                rulez.field["entity_uuid"] == model.entity().uuid,
                rulez.field["entity_content_uuid"] == model.uuid,
            )
        )

        data = {}
        for keyidx in [i[0] for i in col.index_attrs()]:
            res = self.request.app.get_indexer(model, keyidx)
            data[keyidx] = res

        if existing:
            existing[0].update(data)
            result = existing[0]
        else:
            result = idxcol.create(data, deserialize=False)

        return result

    def unindex(self, model):
        idxcol = self.request.get_collection("morpcc.index").content_collection()

        existing = idxcol.search(
            rulez.and_(
                rulez.field["application_uuid"] == model.entity().application().uuid,
                rulez.field["entity_uuid"] == model.entity().uuid,
                rulez.field["entity_content_uuid"] == model.uuid,
            )
        )

        if existing:
            existing[0].delete(permanent=True)

    def drop_all(self):
        for ec in self.entity_collections().values():
            ec.drop_all()


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
