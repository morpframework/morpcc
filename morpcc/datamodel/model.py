import typing
from dataclasses import field, make_dataclass

import morpfw
import rulez
from morpcc.deform.referencewidget import ReferenceWidget
from morpfw.crud.storage.pgsqlstorage import PgSQLStorage
from sqlalchemy import MetaData

from ..attribute.path import get_collection as get_attribute_collection
from ..backrelationship.path import \
    get_collection as get_backrelationship_collection
from ..relationship.path import get_collection as get_relationship_collection
from ..relationship.widget import DataModelContentReferenceWidget
from .modelui import (DataModelCollectionUI, DataModelContentCollectionUI,
                      DataModelContentModelUI, DataModelModelUI)
from .schema import DataModelSchema


class DataModelContentCollection(morpfw.Collection):
    def __init__(self, parent, request, storage, data=None):
        self.__parent__ = parent
        super().__init__(request, storage, data=data)

    def ui(self):
        return DataModelContentCollectionUI(self.request, self)

    @property
    def schema(self):
        return self.__parent__.dataclass()


class DataModelContentModel(morpfw.Model):
    @property
    def schema(self):
        return self.collection.schema

    def ui(self):
        return DataModelContentModelUI(self.request, self, self.collection.ui())

    def attributes(self):
        datamodel = self.collection.__parent__
        return datamodel.attributes()

    def relationships(self):
        datamodel = self.collection.__parent__
        return datamodel.relationships()

    def backrelationships(self):
        datamodel = self.collection.__parent__
        return datamodel.backrelationships()

    def datamodel(self):
        return self.collection.__parent__


class DataModelModel(morpfw.Model):
    schema = DataModelSchema

    def ui(self):
        return DataModelModelUI(self.request, self, self.collection.ui())

    def dataclass(self):

        attrs = []
        for k, attr in self.attributes().items():
            metadata = {
                "required": attr["required"],
                "title": attr["title"],
                "description": attr["description"],
            }
            attrs.append(
                (attr["name"], attr.datatype(), field(default=None, metadata=metadata))
            )

        for r, rel in self.relationships().items():
            refsearch = rel.reference_search_attribute()
            ref = rel.reference_attribute()
            ref_field = ref["name"]
            if refsearch:
                refsearch_field = refsearch["name"]
            else:
                refsearch_field = ref["name"]

            dm = ref.datamodel()

            if refsearch:
                # refsearch field and ref field must come from the same datamodel
                assert dm["uuid"] == refsearch.datamodel()["uuid"]
            metadata = {
                "required": rel["required"],
                "title": rel["title"],
                "description": rel["description"],
                "deform.widget": DataModelContentReferenceWidget(
                    datamodel=dm, term_field=refsearch_field, value_field=ref_field
                ),
            }

            attrs.append(
                (rel["name"], rel.datatype(), field(default=None, metadata=metadata))
            )

        name = self["name"] or "Model"
        return make_dataclass(name, fields=attrs, bases=(morpfw.Schema,))

    def attributes(self):
        attrcol = get_attribute_collection(self.request)
        attrs = attrcol.search(rulez.field["datamodel_uuid"] == self.uuid)
        result = {}

        for attr in attrs:
            result[attr["name"]] = attr

        return result

    def relationships(self):
        relcol = get_relationship_collection(self.request)
        rels = relcol.search(rulez.field["datamodel_uuid"] == self.uuid)

        result = {}

        for rel in rels:
            result[rel["name"]] = rel

        return result

    def backrelationships(self):
        brelcol = get_backrelationship_collection(self.request)
        brels = brelcol.search(rulez.field["datamodel_uuid"] == self.uuid)
        result = {}
        for brel in brels:
            result[brel["name"]] = brel

        return result

    def application(self):
        from ..application.path import get_model as get_app

        dmapp = get_app(self.request, self["application_uuid"])
        return dmapp

    def content_metadata(self):
        dmapp = self.application()
        return dmapp.content_metadata()

    def content_collection(self):
        class Model(DataModelContentModel):
            schema = self.dataclass()

            __path_model__ = DataModelContentModel

        class Collection(DataModelContentCollection):

            __path_model__ = DataModelContentCollection

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


class DataModelCollection(morpfw.Collection):
    schema = DataModelSchema

    def ui(self):
        return DataModelCollectionUI(self.request, self)
