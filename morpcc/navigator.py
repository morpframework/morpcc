import typing

import rulez
from morpcc.attribute.model import AttributeModel
from morpcc.dictionaryelement.model import DictionaryElementModel
from morpcc.relationship.model import RelationshipModel
from morpcc.schema.model import SchemaModel

from .app import App
from .entitycontent.path import content_collection_factory


class AttributesBrowser(object):
    def __init__(self, entity, request):
        self.entity = entity
        self.col = request.get_collection("morpcc.attribute")

    def __getitem__(self, key):
        attrs = self.col.search(
            rulez.and_(
                rulez.field["entity_uuid"] == self.entity.uuid,
                rulez.field["name"] == key,
            )
        )
        if attrs:
            return attrs[0]
        return None

    def keys(self) -> typing.List[str]:
        return [
            i["name"]
            for i in self.col.search(rulez.field["entity_uuid"] == self.entity.uuid)
        ]


class RelationshipsBrowser(AttributesBrowser):
    def __init__(self, entity, request):
        self.entity = entity
        self.col = request.get_collection("morpcc.relationship")


class BackRelationshipsBrowser(AttributesBrowser):
    def __init__(self, entity, request):
        self.entity = entity
        self.col = request.get_collection("morpcc.backrelationship")


class EntityNavigator(object):
    def __init__(self, schema, entity, request):
        self.schema = schema
        self.entity = entity
        self.request = request
        self.attr_col = request.get_collection("morpcc.attribute")
        self.rel_col = request.get_collection("morpcc.relationship")
        self.brel_col = request.get_collection("morpcc.backrelationship")
        self.attributes = AttributesBrowser(entity, request)
        self.relationships = RelationshipsBrowser(entity, request)
        self.backrelationships = RelationshipsBrowser(entity, request)

    def add_attribute(
        self,
        name: str,
        type_: str,
        title: str,
        description: typing.Optional[str] = None,
        required: bool = False,
        primary_key: bool = False,
        dictionaryelement: typing.Optional[DictionaryElementModel] = None,
        allow_invalid: bool = False,
    ):
        data = {
            "name": name,
            "type": type_,
            "title": title,
            "description": description,
            "required": required,
            "primary_key": primary_key,
            "entity_uuid": self.entity.uuid,
            "dictionaryelement_uuid": None,
            "allow_invalid": allow_invalid,
        }
        if dictionaryelement:
            data["dictionaryelement_uuid"] = dictionaryelement.uuid

        return self.attr_col.create(data, deserialize=False)

    def add_relationship(
        self,
        name: str,
        title: str,
        reference_attribute: AttributeModel,
        reference_search_attribute: AttributeModel,
        description: typing.Optional[str] = None,
        required: bool = False,
        primary_key: bool = False,
    ):
        data = {
            "name": name,
            "title": title,
            "description": description,
            "reference_attribute_uuid": reference_attribute.uuid,
            "reference_search_attribute_uuid": reference_search_attribute.uuid,
            "required": required,
            "primary_key": primary_key,
            "entity_uuid": self.entity.uuid,
        }

        return self.rel_col.create(data, deserialize=False)

    def add_backrelationship(
        self,
        name: str,
        title: str,
        reference_relationship: RelationshipModel,
        description: typing.Optional[str] = None,
        single_relation: bool = False,
    ):
        data = {
            "name": name,
            "title": title,
            "description": description,
            "entity_uuid": self.entity.uuid,
            "reference_relationship_uuid": reference_relationship.uuid,
            "single_relation": single_relation,
        }

        return self.brel_col.create(data, deserialize=False)


class EntityContentNavigator(object):
    def __init__(self, entity, application, request):
        self.request = request
        self.entity = entity
        self.collection = content_collection_factory(entity, application)
        self.collection_allow_invalid = content_collection_factory(
            entity, application, allow_invalid=True
        )

    def add(self, data, allow_invalid=False):
        if not allow_invalid:
            return self.collection.create(data, deserialize=False)
        else:
            return self.collection_allow_invalid.create(data, deserialize=False)

    def search(self, *args, **kwargs):
        return self.collection.search(*args, **kwargs)

    def get(self, uuid):
        return self.collection.get(uuid)


class EntityContentCollectionBrowser(object):
    def __init__(self, request, application):
        self.request = request
        self.application = application
        self.collection = request.get_collection("morpcc.entity")

    def __getitem__(self, key) -> EntityContentNavigator:
        items = self.collection.search(
            rulez.and_(
                rulez.field["name"] == key,
                rulez.field["schema_uuid"]
                == self.application.application_schema().uuid,
            )
        )
        if items:
            return EntityContentNavigator(items[0], self.application, self.request)
        raise KeyError(key)

    def keys(self) -> typing.List[str]:
        schema: SchemaModel = self.application.application_schema()
        return [e["name"] for e in schema.entities()]


class ApplicationNavigator(object):
    def __init__(self, application, request):
        self.application = application
        self.request = request
        self.entities = EntityContentCollectionBrowser(request, application)

    def __getitem__(self, key) -> EntityContentNavigator:
        return self.entities[key]

    def keys(self):
        return self.entities.keys()

    def values(self) -> typing.List[EntityNavigator]:
        return self.entities.values()


class RefDataKeyNavigator(object):
    def __init__(self, refdatakey, request):
        self.refdatakey = refdatakey
        self.request = request
        self.prop_col = request.get_collection("morpcc.referencedataproperty")

    def add_property(self, name, value):
        data = {
            "name": name,
            "value": value,
            "referencedatakey_uuid": self.refdatakey.uuid,
        }
        prop = self.prop_col.create(data, deserialize=False)
        return prop

    def __getitem__(self, key):
        props = self.prop_col.search(
            rulez.and_(
                rulez.field["referencedatakey_uuid"] == self.refdatakey.uuid,
                rulez.field["name"] == key,
            )
        )
        if props:
            return props[0]
        return KeyError(key)

    def keys(self) -> typing.List[str]:
        return [
            p["name"]
            for p in self.prop_col.search(
                rulez.field["referencedatakey_uuid"] == self.refdatakey.uuid
            )
        ]


class RefDataNavigator(object):
    def __init__(self, refdata, request):
        self.refdata = refdata
        self.request = request
        self.key_col = request.get_collection("morpcc.referencedatakey")

    def add_key(
        self, name: str, description: typing.Optional[str] = None
    ) -> typing.Optional[RefDataKeyNavigator]:
        data = {
            "name": name,
            "referencedata_uuid": self.refdata.uuid,
            "description": description,
        }
        key = self.key_col.create(data, deserialize=False)
        if key:
            return RefDataKeyNavigator(key, self.request)
        return None

    def __getitem__(self, key) -> RefDataKeyNavigator:
        keys = self.key_col.search(
            rulez.and_(
                rulez.field["referencedata_uuid"] == self.refdata.uuid,
                rulez.field["name"] == key,
            )
        )
        if keys:
            return RefDataKeyNavigator(keys[0], self.request)
        raise KeyError(key)

    def keys(self) -> typing.List[str]:
        return [
            k["name"]
            for k in self.key_col.search(
                rulez.field["referencedata_uuid"] == self.refdata.uuid
            )
        ]


class DictionaryEntityNavigator(object):
    def __init__(self, dictentity, request):
        self.dictentity = dictentity
        self.request = request
        self.element_col = request.get_collection("morpcc.dictionaryelement")

    def add_element(
        self,
        name: str,
        title: str,
        type_: str,
        referencedata_name: typing.Optional[str] = None,
        referencedata_property: str = "label",
    ):
        data = {
            "name": name,
            "title": title,
            "type": type_,
            "dictionaryentity_uuid": self.dictentity.uuid,
            "referencedata_name": referencedata_name,
            "referencedata_property": referencedata_property,
        }
        el = self.element_col.create(data, deserialize=False)
        return el

    def __getitem__(self, key):
        elements = self.element_col.search(
            rulez.and_(
                rulez.field["dictionaryentity_uuid"] == self.dictentity.uuid,
                rulez.field["name"] == key,
            )
        )
        if elements:
            return elements[0]
        raise KeyError(key)

    def keys(self) -> typing.List[str]:
        return [
            e["name"]
            for e in self.element_col.search(
                rulez.field["dictionaryentity_uuid"] == self.dictentity.uuid
            )
        ]


class DataDictionaryBrowser(object):
    def __init__(self, request):
        self.request = request
        self.dictentity_col = request.get_collection("morpcc.dictionaryentity")

    def __getitem__(self, key) -> DictionaryEntityNavigator:
        dents = self.dictentity_col.search(rulez.field["name"] == key)
        if dents:
            return DictionaryEntityNavigator(dents[0], self.request)
        raise KeyError(key)

    def keys(self) -> typing.List[str]:
        return [e["name"] for e in self.dictentity_col.search()]


class EntityBrowser(object):
    def __init__(self, schema, request):
        self.schema = schema
        self.request = request
        self.collection = request.get_collection("morpcc.entity")

    def __getitem__(self, key) -> EntityNavigator:
        items = self.collection.search(
            rulez.and_(
                rulez.field["schema_uuid"] == self.schema.uuid,
                rulez.field["name"] == key,
            )
        )
        if items:
            return EntityNavigator(self.schema, items[0], self.request)
        raise KeyError(key)

    def keys(self) -> typing.List[str]:
        return [
            e["name"]
            for e in self.collection.search(
                rulez.field["schema_uuid"] == self.schema.uuid
            )
        ]


class SchemaNavigator(object):
    def __init__(self, schema, request):
        self.schema = schema
        self.request = request
        self.entity_col = request.get_collection("morpcc.entity")
        self.entities = EntityBrowser(schema, request)

    def add_entity(
        self, name: str, title: str, icon: str = "database"
    ) -> typing.Optional[EntityNavigator]:
        data = {
            "name": name,
            "title": title,
            "icon": icon,
            "schema_uuid": self.schema.uuid,
        }
        entity = self.entity_col.create(data, deserialize=False)
        if entity:
            return EntityNavigator(self.schema, entity, self.request)
        return None

    def keys(self):
        return self.entities.keys()

    def __getitem__(self, key):
        return self.entities[key]


class SchemaBrowser(object):
    def __init__(self, request):
        self.request = request
        self.collection = request.get_collection("morpcc.schema")

    def __getitem__(self, key) -> SchemaNavigator:
        items = self.collection.search(rulez.field["name"] == key)
        if items:
            return SchemaNavigator(items[0], self.request)
        raise KeyError(key)

    def keys(self) -> typing.List[str]:
        return [e["name"] for e in self.collection.search()]


class ApplicationBrowser(object):
    def __init__(self, request):
        self.request = request
        self.collection = request.get_collection("morpcc.application")

    def __getitem__(self, key) -> ApplicationNavigator:
        items = self.collection.search(rulez.field["name"] == key)
        if items:
            return ApplicationNavigator(items[0], self.request)
        raise KeyError(key)

    def keys(self) -> typing.List[str]:
        return [e["name"] for e in self.collection.search()]


class Navigator(object):
    def __init__(self, request):
        self.request = request
        self.app_col = request.get_collection("morpcc.application")
        self.refdata_col = request.get_collection("morpcc.referencedata")
        self.dictentity_col = request.get_collection("morpcc.dictionaryentity")
        self.schema_col = request.get_collection("morpcc.schema")
        self.datadictionary = DataDictionaryBrowser(request)
        self.schemas = SchemaBrowser(request)
        self.applications = ApplicationBrowser(request)

    def get_application(self, app_uuid) -> ApplicationNavigator:
        col = self.request.get_collection("morpcc.application")
        app = col.get(app_uuid)
        if app:
            return ApplicationNavigator(app, self.request)

    def add_schema(
        self, name: str, title: str, icon: str = "cube"
    ) -> typing.Optional[SchemaNavigator]:
        data = {"name": name, "title": title}
        schema = self.schema_col.create(data, deserialize=False)
        if schema:
            return SchemaNavigator(schema, self.request)
        return None

    def add_application(
        self, name: str, title: str, schema: SchemaModel, icon: str = "cube"
    ) -> typing.Optional[ApplicationNavigator]:
        data = {
            "name": name,
            "title": title,
            "icon": icon,
            "schema_uuid": schema.uuid,
        }
        app = self.app_col.create(data, deserialize=False)
        if app:
            return ApplicationNavigator(app, self.request)
        return None

    def add_referencedata(
        self, name: str, title: str
    ) -> typing.Optional[RefDataNavigator]:
        data = {"name": name, "title": title}
        refdata = self.refdata_col.create(data, deserialize=False)
        if refdata:
            return RefDataNavigator(refdata, self.request)
        return None

    def add_dictionaryentity(
        self, name: str, title: str
    ) -> typing.Optional[DictionaryEntityNavigator]:
        data = {"name": name, "title": title}
        dent = self.dictentity_col.create(data, deserialize=False)
        if dent:
            return DictionaryEntityNavigator(dent, self.request)
        return None
