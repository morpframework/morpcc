from dataclasses import field, make_dataclass

from sqlalchemy import DDL, MetaData

import morpfw
import rulez
from morpfw.crud import signals
from morpfw.crud.storage.pgsqlstorage import PgSQLStorage

from ..datamodel.model import DataModelContentModel
from ..datamodel.path import get_collection as get_dm_collection
from ..index.model import IndexContentCollection, IndexContentModel
from ..index.path import get_collection as get_index_collection
from .modelui import ApplicationCollectionUI, ApplicationModelUI
from .schema import ApplicationSchema


class ApplicationModel(morpfw.Model):
    schema = ApplicationSchema

    def ui(self):
        return ApplicationModelUI(self.request, self, self.collection.ui())

    def content_metadata(self):
        return MetaData(schema=self["name"])

    def datamodels(self):
        col = get_dm_collection(self.request)
        dms = col.search(rulez.field["application_uuid"] == self.uuid)
        return dms

    def reindex(self):
        for dm in self.datamodels():
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
        idxcol = get_index_collection(self.request).content_collection()
        existing = idxcol.search(
            rulez.and_(
                rulez.field["application_uuid"] == model.datamodel().application().uuid,
                rulez.field["datamodel_uuid"] == model.datamodel().uuid,
                rulez.field["datamodel_content_uuid"] == model.uuid,
            )
        )

        data = {}
        for keyidx in [
            "application_uuid",
            "datamodel_content_uuid",
            "datamodel_uuid",
            "searchabletext",
        ]:
            res = self.request.app.get_indexer(model, keyidx)
            assert res is not None
            data[keyidx] = res.lower()

        for idx in get_index_collection(self.request).search():
            res = self.request.app.get_indexer(model, idx["name"])
            if res:
                data[idx["name"]] = res.lower()

        if existing:
            existing[0].update(data)
            result = existing[0]
        else:
            result = idxcol.create(data, deserialize=False)

        return result

    def unindex(self, model):
        idxcol = get_index_collection(self.request).content_collection()

        existing = idxcol.search(
            rulez.and_(
                rulez.field["application_uuid"] == model.datamodel().application().uuid,
                rulez.field["datamodel_uuid"] == model.datamodel().uuid,
                rulez.field["datamodel_content_uuid"] == model.uuid,
            )
        )

        if existing:
            existing[0].delete(permanent=True)


class ApplicationCollection(morpfw.Collection):
    schema = ApplicationSchema

    def ui(self):
        return ApplicationCollectionUI(self.request, self)
