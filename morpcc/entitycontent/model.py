import morpfw
import rulez
from morpfw.crud.schemaconverter.dataclass2avsc import dataclass_to_avsc
from morpfw.crud.schemaconverter.dataclass2colanderavro import dataclass_to_colanderavro
from morpfw.crud.storage.pgsqlstorage import PgSQLStorage

from ..relationship.validator import EntityContentReferenceValidator
from ..relationship.widget import EntityContentReferenceWidget
from .modelui import EntityContentCollectionUI, EntityContentModelUI


class EntityContentCollection(morpfw.Collection):
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

    def avro_schema(self):
        entity = self.__parent__
        result = dataclass_to_avsc(self.schema, self.request, namespace=entity["name"])
        for name, rel in self.relationships().items():
            ref_entity = rel.reference_entity()

        for name, brel in self.backrelationships().items():
            ref_entity = brel.reference_entity()
            item_schema = dataclass_to_avsc(
                content_collection_factory(ref_entity, self.__application__).schema,
                request=self.request,
                namespace="%s.%s" % (entity["name"], ref_entity["name"]),
            )

            if brel["single_relation"]:
                field = {"name": name, "type": item_schema}
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

    def resolve_relationship(self, relationship):
        """ return the modelcontent of the relationship """
        attr = relationship.reference_attribute()
        entity = attr.entity()

        col = content_collection_factory(entity, self.collection.__application__)
        res = col.search(rulez.field[attr["name"]] == self[relationship["name"]])
        if res:
            return res[0]
        return None

    def resolve_backrelationship(self, backrelationship):
        rel = backrelationship.reference_relationship()
        dm = rel.entity()
        col = content_collection_factory(dm, self.collection.__application__)

        attr = rel.reference_attribute()

        result = col.search(rulez.field[rel["name"]] == self[attr["name"]])
        return result

    @morpfw.requestmemoize()
    def json(self):
        result = self.base_json()
        for name, rel in self.relationships().items():
            item = self.resolve_relationship(rel)
            result[name] = item.base_json()
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
        cschema = dataclass_to_colanderavro(
            self.schema, exclude_fields=exclude_fields, request=self.request
        )
        cs = cschema()
        cs.bind(context=self, request=self.request)
        return cs.serialize(self.data.as_dict())

    @morpfw.requestmemoize()
    def avro_json(self):
        result = self.base_avro_json()
        for name, rel in self.relationships().items():
            item = self.resolve_relationship(rel)
            result[name] = item.base_avro_json()
        for name, brel in self.backrelationships().items():
            items = self.resolve_backrelationship(brel)
            if brel["single_relation"]:
                if items:
                    result[name] = items[0].base_avro_json()
                else:
                    result[name] = {}
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


def content_collection_factory(entity, application, allow_invalid=False):
    behaviors = entity.behaviors()
    model_markers = []
    modelui_markers = []
    collection_markers = []
    collectionui_markers = []

    for appbehavior in application.behaviors():
        entity_behaviors = getattr(appbehavior, "entity_behaviors", {})
        entity_behavior = entity_behaviors.get(entity["name"], None)
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
        validators=field_validators, widgets=field_widgets, allow_invalid=allow_invalid
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

    return Collection(
        application,
        entity,
        entity.request,
        storage=Storage(entity.request, metadata=application.content_metadata()),
    )
