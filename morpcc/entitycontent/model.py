import copy

import morpfw
import rulez
from inverter import dc2avsc, dc2colanderavro
from morpfw.crud.storage.pgsqlstorage import PgSQLStorage

from ..relationship.validator import EntityContentReferenceValidator
from ..relationship.widget import EntityContentReferenceWidget
from .modelui import EntityContentCollectionUI, EntityContentModelUI


class EntityContentCollection(morpfw.Collection):
    @property
    def name(self):
        app = self.application()
        entity = self.entity()
        return "morpcc.application.%s.%s" % (app["name"], entity["name"])

    def __init__(self, application, parent, request, storage, data=None):
        self.__application__ = application
        self.__parent__ = parent
        super().__init__(request, storage, data=data)

    def ui(self):
        return EntityContentCollectionUI(self.request, self)

    def entity(self):
        return self.__parent__

    def application(self):
        return self.__application__

    def base_avro_schema(self):
        entity = self.__parent__
        result = dc2avsc.convert(
            self.schema,
            request=self.request,
            namespace=entity["name"],
            ignore_required=True,
        )
        return result

    def avro_schema(self):
        entity = self.__parent__
        result = dc2avsc.convert(
            self.schema, request=self.request, namespace=entity["name"]
        )
        for name, rel in self.relationships().items():
            ref_entity = rel.reference_attribute().entity()
            item_schema = dc2avsc.convert(
                content_collection_factory(ref_entity, self.__application__).schema,
                request=self.request,
                namespace="%s.%s" % (entity["name"], ref_entity["name"]),
                ignore_required=True,
            )

            field = {"name": name, "type": [item_schema, "null"]}

            for idx, v in enumerate(result["fields"]):
                if v["name"] == name:
                    result["fields"][idx] = field

        for name, brel in self.backrelationships().items():
            ref_entity = brel.reference_entity()
            item_schema = dc2avsc.convert(
                content_collection_factory(ref_entity, self.__application__).schema,
                request=self.request,
                namespace="%s.%s" % (entity["name"], ref_entity["name"]),
                ignore_required=True,
            )

            if brel["single_relation"]:
                field = {"name": name, "type": [item_schema, "null"]}
            else:
                field = {
                    "name": name,
                    "type": {"type": "array", "items": item_schema},
                }
            # print(field)
            result["fields"].append(field)

        return result

    @morpfw.requestmemoize()
    def memoize_call(self, func, *args):
        return func(self, *args)

    def attributes(self):
        return self.__parent__.attributes()

    def relationships(self):
        return self.__parent__.relationships()

    def backrelationships(self):
        return self.__parent__.backrelationships()

    def validation_dict(self, data):
        result = copy.deepcopy(data)
        for name, rel in self.relationships().items():
            item = self.resolve_relationship(rel, data)
            if item:
                result[name] = item.as_dict()
        for name, brel in self.backrelationships().items():
            items = self.resolve_backrelationship(brel, data)
            if brel["single_relation"]:
                if items:
                    result[name] = items[0].as_dict()
                else:
                    result[name] = {}
            else:
                result[name] = [item.as_dict() for item in items if item is not None]
        return result

    def resolve_relationship(self, relationship, data, allow_invalid=False):
        """ return the modelcontent of the relationship """
        if not relationship["name"] in data:
            return None
        attr = relationship.reference_attribute()
        entity = attr.entity()

        col = content_collection_factory(
            entity, self.__application__, allow_invalid=allow_invalid
        )
        res = col.search(rulez.field[attr["name"]] == data[relationship["name"]])
        if res:
            return res[0]
        return None

    def resolve_backrelationship(self, backrelationship, data, allow_invalid=False):
        rel = backrelationship.reference_relationship()
        dm = rel.entity()
        col = content_collection_factory(
            dm, self.__application__, allow_invalid=allow_invalid
        )

        attr = rel.reference_attribute()

        if not attr["name"] in data:
            return []

        result = col.search(rulez.field[rel["name"]] == data[attr["name"]])
        return result

    def drop_all(self):
        app = self.application()
        meta = app.content_metadata()
        bind = self.storage.session.bind
        meta.reflect(bind)
        meta.tables["%s.%s" % (app["name"], self.entity()["name"])].drop(bind)


class EntityContentModel(morpfw.Model):
    @property
    def schema(self):
        return self.collection.schema

    def ui(self):
        return EntityContentModelUI(self.request, self, self.collection.ui())

    def title(self):
        title_parts = []
        for attrname, attr in self.attributes().items():
            if attr["primary_key"]:
                title_parts.append(self[attrname])
        if not title_parts:
            return self["uuid"]
        return ", ".join(title_parts)

    def application(self):
        return self.collection.application()

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

    def resolve_relationship(self, relationship, allow_invalid=False):
        """ return the modelcontent of the relationship """
        attr = relationship.reference_attribute()
        entity = attr.entity()

        col = content_collection_factory(
            entity, self.collection.__application__, allow_invalid=allow_invalid
        )
        res = col.search(rulez.field[attr["name"]] == self[relationship["name"]])
        if res:
            return res[0]
        return None

    def resolve_backrelationship(self, backrelationship, allow_invalid=False):
        rel = backrelationship.reference_relationship()
        dm = rel.entity()
        col = content_collection_factory(
            dm, self.collection.__application__, allow_invalid=allow_invalid
        )

        attr = rel.reference_attribute()

        result = col.search(rulez.field[rel["name"]] == self[attr["name"]])
        return result

    @morpfw.requestmemoize()
    def json(self):
        result = self.base_json()
        for name, rel in self.relationships().items():
            item = self.resolve_relationship(rel)
            if item:
                result[name] = item.base_json()
            else:
                result[name] = None
        for name, brel in self.backrelationships().items():
            items = self.resolve_backrelationship(brel)
            if brel["single_relation"]:
                if items:
                    result[name] = items[0].base_json()
                else:
                    result[name] = {}
            else:
                result[name] = [item.base_json() for item in items]
        return result

    @morpfw.requestmemoize()
    def base_avro_json(self):
        exclude_fields = self.hidden_fields
        cschema = dc2colanderavro.convert(
            self.schema, exclude_fields=exclude_fields, request=self.request
        )
        cs = cschema()
        cs = cs.bind(context=self, request=self.request)
        return cs.serialize(self.data.as_dict())

    @morpfw.requestmemoize()
    def avro_json(self):
        result = self.base_avro_json()
        for name, rel in self.relationships().items():
            item = self.resolve_relationship(rel)
            if item:
                result[name] = item.base_avro_json()
        for name, brel in self.backrelationships().items():
            items = self.resolve_backrelationship(brel)
            if brel["single_relation"]:
                if items:
                    result[name] = items[0].base_avro_json()
                else:
                    result[name] = None
            else:
                result[name] = [item.base_avro_json() for item in items]
        return result

    @morpfw.requestmemoize()
    def validation_dict(self):
        result = self.as_dict()
        for name, rel in self.relationships().items():
            item = self.resolve_relationship(rel)
            if item:
                result[name] = item.as_dict()
        for name, brel in self.backrelationships().items():
            items = self.resolve_backrelationship(brel)
            if brel["single_relation"]:
                if items:
                    result[name] = items[0].as_dict()
                else:
                    result[name] = {}
            else:
                result[name] = [item.as_dict() for item in items if item is not None]
        return result

    def validation_failures(self):
        entity = self.entity()
        data = self.validation_dict()
        result = {"entity_validator": [], "attribute_validator": {}}
        for validator in entity.entity_validators():
            validate = validator.function()
            if not validate(data):
                result["entity_validator"].append(validator["name"])

        for attrname, attr in entity.attributes().items():
            for validator in attr.builtin_validators():
                validate = validator["validate"]
                if not validate(self[attrname]):
                    result["attribute_validator"].setdefault(attrname, [])
                    result["attribute_validator"][attrname].append(validator["name"])

            for validator in attr.validators():
                validate = validator.function()
                if not validate(self[attrname]):
                    result["attribute_validator"].setdefault(attrname, [])
                    result["attribute_validator"][attrname].append(validator["name"])
        return result


def content_collection_factory(entity, application, allow_invalid=False):
    request = application.request
    cache_key = "-".join(
        [application["uuid"], entity["uuid"], "1" if allow_invalid else "0"]
    )
    request.environ.setdefault("morpcc.cache.content_collection", {})
    cachemgr = request.environ["morpcc.cache.content_collection"]
    if cache_key in cachemgr:
        return cachemgr[cache_key]

    behaviors = entity.behaviors()
    model_markers = []
    modelui_markers = []
    collection_markers = []
    collectionui_markers = []

    for appbehavior in application.behaviors():
        entity_behaviors = getattr(appbehavior, "entity_behaviors", {})
        entity_behavior = entity_behaviors.get(entity["name"], None)

        all_entity_behavior = entity_behaviors.get("*", None)
        if all_entity_behavior:
            model_markers.append(all_entity_behavior.model_marker)
            modelui_markers.append(all_entity_behavior.modelui_marker)
            collection_markers.append(all_entity_behavior.collection_marker)
            collectionui_markers.append(all_entity_behavior.collectionui_marker)
        if entity_behavior:
            model_markers.append(entity_behavior.model_marker)
            modelui_markers.append(entity_behavior.modelui_marker)
            collection_markers.append(entity_behavior.collection_marker)
            collectionui_markers.append(entity_behavior.collectionui_marker)

    for behavior in behaviors:
        model_markers.append(behavior.model_marker)
        modelui_markers.append(behavior.modelui_marker)
        collection_markers.append(behavior.collection_marker)
        collectionui_markers.append(behavior.collectionui_marker)

    modelui_markers.append(EntityContentModelUI)

    ModelUI = type("ModelUI", tuple(modelui_markers), {})

    # set relationship widgets and validators
    field_widgets = {}
    field_validators = {}
    for relname, rel in entity.relationships().items():
        refsearch = rel.reference_search_attribute()
        ref = rel.reference_attribute()
        ref_field = ref["name"]
        if refsearch:
            refsearch_field = refsearch["name"]
        else:
            refsearch_field = ref["name"]

        field_validators.setdefault(relname, [])

        if not allow_invalid:
            field_validators[relname].append(
                EntityContentReferenceValidator(
                    application_uuid=application.uuid,
                    entity_uuid=ref["entity_uuid"],
                    attribute=ref_field,
                )
            )

        field_widgets[relname] = EntityContentReferenceWidget(
            application_uuid=application.uuid,
            entity_uuid=ref["entity_uuid"],
            term_field=refsearch_field,
            value_field=ref_field,
        )

    dc_schema = entity.dataclass(
        application.uuid,
        validators=field_validators,
        widgets=field_widgets,
        allow_invalid=allow_invalid,
    )

    class ContentCollectionUI(EntityContentCollectionUI):
        schema = dc_schema
        modelui_class = ModelUI

    collectionui_markers.append(ContentCollectionUI)

    CollectionUI = type("CollectionUI", tuple(collectionui_markers), {})

    class ContentModel(EntityContentModel):

        schema = dc_schema
        __path_model__ = EntityContentModel

        def ui(self):
            return ModelUI(self.request, self, self.collection.ui())

    model_markers.append(ContentModel)

    Model = type("Model", tuple(model_markers), {})

    class ContentCollection(EntityContentCollection):

        schema = dc_schema

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

    result = Collection(
        application,
        entity,
        entity.request,
        storage=Storage(entity.request, metadata=application.content_metadata()),
    )

    cachemgr[cache_key] = result
    return result
