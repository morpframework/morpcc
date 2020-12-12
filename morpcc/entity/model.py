import typing
from dataclasses import field, make_dataclass

import morpfw
import rulez
from morpfw.crud.storage.pgsqlstorage import PgSQLStorage
from sqlalchemy import MetaData

from ..deform.refdatawidget import ReferenceDataWidget
from ..deform.referencewidget import ReferenceWidget
from ..entitycontent.relationship import BackReference, Reference
from ..validator.reference import ReferenceValidator
from .modelui import EntityCollectionUI, EntityModelUI
from .schema import EntitySchema


class EntityModel(morpfw.Model):
    schema = EntitySchema

    def ui(self):
        return EntityModelUI(self.request, self, self.collection.ui())

    def title(self):
        return self["title"]

    def icon(self):
        return self["icon"] or "database"

    def dataclass(
        self, application_uuid, validators=None, widgets=None, allow_invalid=False
    ):
        validators = validators or {}
        widgets = widgets or {}
        attrs = []
        primary_key = []
        brels = [
            b["reference_relationship_uuid"] for b in self.backrelationships().values()
        ]

        allow_invalid = allow_invalid or self["allow_invalid"]
        for k, attr in self.attributes().items():
            if not allow_invalid:
                metadata = attr.field_metadata()
            else:
                metadata = attr.field_metadata_allow_invalid()

            if attr.uuid in brels:
                metadata["index"] = True

            name = attr["name"]
            if validators.get(name, []):
                metadata.setdefault("validators", [])
                metadata["validators"] += validators[name]
            if widgets.get(k, None):
                metadata["deform.widget"] = widgets[name]
            attrs.append(
                (attr["name"], attr.datatype(), field(default=None, metadata=metadata))
            )
            if attr["primary_key"]:
                primary_key.append(attr["name"])

        for r, rel in self.relationships().items():
            refsearch = rel.reference_search_attribute()
            ref = rel.reference_attribute()
            dm = ref.entity()

            if refsearch:
                # refsearch field and ref field must come from the same entity
                assert dm["uuid"] == refsearch.entity()["uuid"]
            metadata = {
                "required": rel["required"],
                "title": rel["title"],
                "description": rel["description"],
                "validators": [],
                "index": True,
            }

            name = rel["name"]
            if validators.get(name, []):
                metadata.setdefault("validators", [])
                metadata["validators"] += validators[name]
            if widgets.get(name, None):
                metadata["deform.widget"] = widgets[name]

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

        if not allow_invalid:
            dc.__validators__ = [
                ev.schema_validator() for ev in self.entity_validators()
            ]

        references = []
        for rn, rel in self.relationships().items():
            references.append(
                Reference(
                    rn,
                    application_uuid,
                    rel.reference_entity().uuid,
                    attribute=rel.reference_attribute()["name"],
                    title=rel["title"],
                )
            )
        dc.__references__ = references

        backreferences = []
        for rn, brel in self.backrelationships().items():
            backreferences.append(
                BackReference(
                    brel["name"],
                    application_uuid,
                    brel.reference_entity().uuid,
                    brel.reference_relationship()["name"],
                    title=brel["title"],
                    single=brel["single_relation"],
                )
            )
        dc.__backreferences__ = backreferences
        return dc

    @morpfw.requestmemoize()
    def attributes(self):
        attrcol = self.request.get_collection("morpcc.attribute")
        attrs = attrcol.search(
            rulez.field["entity_uuid"] == self.uuid, order_by=("order", "asc")
        )
        result = {}

        for attr in attrs:
            result[attr["name"]] = attr

        return result

    @morpfw.requestmemoize()
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

    @morpfw.requestmemoize()
    def relationships(self):
        relcol = self.request.get_collection("morpcc.relationship")
        rels = relcol.search(rulez.field["entity_uuid"] == self.uuid)

        result = {}

        for rel in rels:
            result[rel["name"]] = rel

        return result

    @morpfw.requestmemoize()
    def backrelationships(self):
        brelcol = self.request.get_collection("morpcc.backrelationship")
        brels = brelcol.search(rulez.field["entity_uuid"] == self.uuid)
        result = {}
        for brel in brels:
            result[brel["name"]] = brel

        return result

    @morpfw.requestmemoize()
    def behaviors(self):
        bhvcol = self.request.get_collection("morpcc.behaviorassignment")
        assignments = bhvcol.search(rulez.field["entity_uuid"] == self.uuid)
        behaviors = []
        for assignment in assignments:
            behavior = self.request.app.config.behavior_registry.get_behavior(
                assignment["behavior"], self.request
            )
            behaviors.append(behavior)

        return behaviors

    @morpfw.requestmemoize()
    def entity_schema(self):
        col = self.request.get_collection("morpcc.schema")
        schema = col.get(self["schema_uuid"])
        return schema

    @morpfw.requestmemoize()
    def entity_validators(self):
        col = self.request.get_collection("morpcc.entityvalidatorassignment")
        assignments = col.search(rulez.field["entity_uuid"] == self.uuid)
        validators = [v.validator() for v in assignments]
        return validators

    @morpfw.requestmemoize()
    def get_entity_validator(self, name):
        for v in self.entity_validators():
            if v["name"] == name:
                return v


class EntityCollection(morpfw.Collection):
    schema = EntitySchema

    def ui(self):
        return EntityCollectionUI(self.request, self)
