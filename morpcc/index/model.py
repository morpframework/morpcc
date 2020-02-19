from dataclasses import field, make_dataclass

import morpfw
from morpfw.crud.storage.pgsqlstorage import PgSQLStorage
from sqlalchemy import MetaData

from .modelui import (
    IndexCollectionUI,
    IndexContentCollectionUI,
    IndexContentModelUI,
    IndexModelUI,
)
from .schema import IndexSchema


class IndexContentModel(morpfw.Model):
    def ui(self):
        return IndexContentModelUI(self.request, self, self.collection.ui())


class IndexContentCollection(morpfw.Collection):
    pass


class IndexModel(morpfw.Model):
    schema = IndexSchema

    def ui(self):
        return IndexModelUI(self.request, self, self.collection.ui())


class IndexCollection(morpfw.Collection):
    schema = IndexSchema

    def ui(self):
        return IndexCollectionUI(self.request, self)

    def content_metadata(self):
        return MetaData(schema="morpfw_catalog")

    def content_collection(self):
        class Model(IndexContentModel):
            schema = self.dataclass()

            __path_model__ = IndexContentModel

        class Collection(IndexContentCollection):
            schema = self.dataclass()

            __path_model__ = IndexContentCollection

            def __init__(self, parent, *args, **kwargs):
                self.__parent__ = parent
                super().__init__(*args, **kwargs)

        class Storage(PgSQLStorage):
            model = Model

            @property
            def session(self):
                return self.request.get_db_session("warehouse")

        return Collection(
            self,
            self.request,
            storage=Storage(self.request, metadata=self.content_metadata()),
        )

    def dataclass(self):
        attrs = [
            ("application_uuid", str, field(default=None, metadata={"format": "uuid"})),
            ("datamodel_uuid", str, field(default=None, metadata={"format": "uuid"})),
            (
                "datamodel_content_uuid",
                str,
                field(default=None, metadata={"format": "uuid"}),
            ),
            (
                "searchabletext",
                str,
                field(default=None, metadata={"format": "fulltextindex"}),
            ),
        ]

        for idx in self.search():
            metadata = {}
            if idx["type"] == "fulltextindex":
                metadata["format"] = "fulltextindex"

            attrs.append((idx["name"], str, field(default=None, metadata=metadata)))

        return make_dataclass("morpcc_catalog", attrs, bases=(morpfw.Schema,))
