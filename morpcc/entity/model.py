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
from ..relationship.widget import EntityContentReferenceWidget
from .modelui import (
    EntityCollectionUI,
    EntityContentCollectionUI,
    EntityContentModelUI,
    EntityModelUI,
)
from .schema import EntitySchema


class EntityContentCollection(morpfw.Collection):
    def __init__(self, parent, request, storage, data=None):
        self.__parent__ = parent
        super().__init__(request, storage, data=data)

    def ui(self):
        return EntityContentCollectionUI(self.request, self)

    @property
    def schema(self):
        return self.__parent__.dataclass()


class EntityContentModel(morpfw.Model):
    @property
    def schema(self):
        return self.collection.schema

    def ui(self):
        return EntityContentModelUI(self.request, self, self.collection.ui())

    def attributes(self):
        entity = self.collection.__parent__
        return entity.attributes()

    def relationships(self):
        entity = self.collection.__parent__
        return entity.relationships()

    def backrelationships(self):
        entity = self.collection.__parent__
        return entity.backrelationships()

    def entity(self):
        return self.collection.__parent__


class EntityModel(morpfw.Model):
    schema = EntitySchema

    def ui(self):
        return EntityModelUI(self.request, self, self.collection.ui())

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

            dm = ref.entity()

            if refsearch:
                # refsearch field and ref field must come from the same entity
                assert dm["uuid"] == refsearch.entity()["uuid"]
            metadata = {
                "required": rel["required"],
                "title": rel["title"],
                "description": rel["description"],
                "deform.widget": EntityContentReferenceWidget(
                    entity=dm, term_field=refsearch_field, value_field=ref_field
                ),
            }

            attrs.append(
                (rel["name"], rel.datatype(), field(default=None, metadata=metadata))
            )

            if rel["primary_key"]:
                primary_key.append(rel["name"])

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
        attrs = attrcol.search(rulez.field["entity_uuid"] == self.uuid)
        result = {}

        for attr in attrs:
            result[attr["name"]] = attr

        return result

    def effective_attributes(self):

        result = {}
        
        attrs = self.attributes()

        for behavior in self.behaviors():
            for n, attr in behavior.schema.__dataclass_fields__.items():
                if n in attrs.keys():
                    continue

                title = n
                if attr.metadata.get("title", None):
                    title = attr.metadata["title"]
                result[n] = {"title": title, "name": n}

        for n, attr in attrs.items():
            result[n] = {"title": attr["title"], "name": n}

        return result


    def relationships(self):
        relcol = get_relationship_collection(self.request)
        rels = relcol.search(rulez.field["entity_uuid"] == self.uuid)

        result = {}

        for rel in rels:
            result[rel["name"]] = rel

        return result

    def backrelationships(self):
        brelcol = get_backrelationship_collection(self.request)
        brels = brelcol.search(rulez.field["entity_uuid"] == self.uuid)
        result = {}
        for brel in brels:
            result[brel["name"]] = brel

        return result

    def behaviors(self):
        bhvcol = get_behaviorassignment_collection(self.request)
        assignments = bhvcol.search(rulez.field["entity_uuid"] == self.uuid)
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

        modelui_markers.append(EntityContentModelUI)

        ModelUI = type("ModelUI", tuple(modelui_markers), {})

        class ContentCollectionUI(EntityContentCollectionUI):

            modelui_class = ModelUI

        collectionui_markers.append(ContentCollectionUI)

        CollectionUI = type("CollectionUI", tuple(collectionui_markers), {})

        class ContentModel(EntityContentModel):
            schema = self.dataclass()

            __path_model__ = EntityContentModel

            def ui(self):
                return ModelUI(self.request, self, self.collection.ui())

        model_markers.append(ContentModel)

        Model = type("Model", tuple(model_markers), {})

        class ContentCollection(EntityContentCollection):

            __path_model__ = EntityContentCollection

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


class EntityCollection(morpfw.Collection):
    schema = EntitySchema

    def ui(self):
        return EntityCollectionUI(self.request, self)
