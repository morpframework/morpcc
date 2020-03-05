import copy
import typing
from dataclasses import field, make_dataclass

import morpfw
import rulez
from morpfw.crud.storage.pgsqlstorage import PgSQLStorage
from sqlalchemy import MetaData

from ..attribute.path import get_collection as get_attribute_collection
from ..backrelationship.path import get_collection as get_backrelationship_collection
from ..behaviorassignment.path import (
    get_collection as get_behaviorassignment_collection,
)
from ..deform.refdatawidget import ReferenceDataWidget
from ..deform.referencewidget import ReferenceWidget
from ..relationship.path import get_collection as get_relationship_collection
from ..relationship.validator import EntityReferenceValidator
from ..relationship.widget import EntityContentReferenceWidget
from ..validator.reference import ReferenceValidator
from .modelui import EntityCollectionUI, EntityModelUI
from .schema import EntitySchema

ENTITY_DATACLASS_CACHE = {}


class EntityModel(morpfw.Model):
    schema = EntitySchema

    def ui(self):
        return EntityModelUI(self.request, self, self.collection.ui())

    def dataclass(self):
        cache = ENTITY_DATACLASS_CACHE.get(self.uuid, None)
        if cache and not (self["modified"] > cache["modified"]):
            return cache["dataclass"]

        attrs = []
        primary_key = []
        brels = [
            b["reference_relationship_uuid"] for b in self.backrelationships().values()
        ]

        for k, attr in self.attributes().items():
            attrmeta = {
                "required": attr["required"],
                "title": attr["title"],
                "description": attr["description"],
            }
            if attr["primary_key"]:
                attrmeta["index"] = True
            if attr.uuid in brels:
                attrmeta["index"] = True
            metadata = attr.field_metadata()
            metadata.update(attrmeta)
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
                "validators": [
                    EntityReferenceValidator(entity_uuid=dm.uuid, attribute=ref_field)
                ],
                "index": True,
                "deform.widget": EntityContentReferenceWidget(
                    entity_uuid=dm.uuid,
                    term_field=refsearch_field,
                    value_field=ref_field,
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
        ENTITY_DATACLASS_CACHE[self.uuid] = {
            "dataclass": dc,
            "modified": self["modified"],
        }
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

    def entity_schema(self):
        from ..schema.path import get_model as get_schema

        schema = get_schema(self.request, self["schema_uuid"])
        return schema


class EntityCollection(morpfw.Collection):
    schema = EntitySchema

    def ui(self):
        return EntityCollectionUI(self.request, self)
