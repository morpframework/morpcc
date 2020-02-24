import typing
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

    def json(self):
        idxcol = self.collection.__parent__
        res = {}
        for idx in idxcol.index_attrs():
            res[idx[0]] = self[idx[0]]
        return res

    def get_object(self):
        resolver = self["index_resolver"]
        if not resolver:
            raise ValueError("Unable to locate resolver")

        resolve = self.request.app.get_index_resolver(resolver)

        return resolve(self, self.request)


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
        return MetaData(schema="morpcc_catalog")

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

    def index_attrs(self):
        attrs = [
            ("title", typing.Optional[str], field(default=None)),
            ("description", typing.Optional[str], field(default=None)),
            ("index_resolver", typing.Optional[str], field(default=None)),
            (
                "application_uuid",
                typing.Optional[str],
                field(default=None, metadata={"format": "uuid"}),
            ),
            (
                "entity_uuid",
                typing.Optional[str],
                field(default=None, metadata={"format": "uuid"}),
            ),
            (
                "entity_content_uuid",
                typing.Optional[str],
                field(default=None, metadata={"format": "uuid"}),
            ),
            (
                "searchabletext",
                typing.Optional[str],
                field(default=None, metadata={"format": "fulltextindex"}),
            ),
        ]

        for idx in self.search():
            metadata = {}
            if idx["type"] == "fulltextindex":
                metadata["format"] = "fulltextindex"

            attrs.append(
                (
                    idx["name"],
                    typing.Optional[str],
                    field(default=None, metadata=metadata),
                )
            )

        return attrs

    def dataclass(self):
        attrs = self.index_attrs()
        return make_dataclass("morpcc_catalog", attrs, bases=(morpfw.Schema,))
