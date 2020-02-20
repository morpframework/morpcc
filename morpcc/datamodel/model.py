import typing
from dataclasses import field, make_dataclass

import morpfw
import rulez
from morpcc.deform.referencewidget import ReferenceWidget
from morpfw.crud.storage.pgsqlstorage import PgSQLStorage
from sqlalchemy import MetaData

from ..attribute.path import get_collection as get_attribute_collection
from ..backrelationship.path import get_collection as get_backrelationship_collection
from ..behaviorassignment.path import (
    get_collection as get_behaviorassignment_collection,
)
from ..relationship.path import get_collection as get_relationship_collection
from ..relationship.widget import DataModelContentReferenceWidget
from .modelui import (
    DataModelCollectionUI,
    DataModelContentCollectionUI,
    DataModelContentModelUI,
    DataModelModelUI,
)
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
        primary_key = []
        for k, attr in self.attributes().items():
            metadata = {
                "required": attr["required"],
                "title": attr["title"],
                "description": attr["description"],
            }
            attrs.append(
                (attr["name"], attr.datatype(), field(default=None, metadata=metadata))
            )
            if attr["primary_key"]:
                primary_key.append(attr["name"])

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
                "format": "uuid",
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

            if attr["primary_key"]:
                primary_key.append(attr["name"])

        name = self["name"] or "Model"

        bases = []
        for behavior in self.behaviors():
            bases.append(behavior.schema)

        bases.append(morpfw.Schema)

        dc = make_dataclass(name, fields=attrs, bases=tuple(bases))
        if primary_key:
            dc.__unique_constraint__ = tuple(primary_key)
        return dc

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

    def behaviors(self):
        bhvcol = get_behaviorassignment_collection(self.request)
        assignments = bhvcol.search(rulez.field["datamodel_uuid"] == self.uuid)
        behaviors = []
        for assignment in assignments:
            behavior = self.request.app.config.behavior_registry.get_behavior(
                assignment["behavior"], self.request
            )
            behaviors.append(behavior)

        return behaviors

    def application(self):
        from ..application.path import get_model as get_app

        dmapp = get_app(self.request, self["application_uuid"])
        return dmapp

    def content_metadata(self):
        dmapp = self.application()
        return dmapp.content_metadata()

    def content_collection(self):
        behaviors = self.behaviors()

        model_markers = []
        modelui_markers = []
        collection_markers = []
        collectionui_markers = []

        for behavior in behaviors:
            model_markers.append(behavior.model_marker)
            modelui_markers.append(behavior.modelui_marker)
            collection_markers.append(behavior.collection_marker)
            collectionui_markers.append(behavior.collectionui_marker)

        modelui_markers.append(DataModelContentModelUI)

        ModelUI = type("ModelUI", tuple(modelui_markers), {})

        class ContentCollectionUI(DataModelContentCollectionUI):

            modelui_class = ModelUI

        collectionui_markers.append(ContentCollectionUI)

        CollectionUI = type("CollectionUI", tuple(collectionui_markers), {})

        class ContentModel(DataModelContentModel):
            schema = self.dataclass()

            __path_model__ = DataModelContentModel

            def ui(self):
                return ModelUI(self.request, self, self.collection.ui())

        model_markers.append(ContentModel)

        Model = type("Model", tuple(model_markers), {})

        class ContentCollection(DataModelContentCollection):

            __path_model__ = DataModelContentCollection

            def ui(self):
                return CollectionUI(self.request, self)

        collection_markers.append(ContentCollection)

        Collection = type("Collection", tuple(collection_markers), {})

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
