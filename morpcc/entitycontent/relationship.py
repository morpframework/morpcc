import rulez

from .model import content_collection_factory


class Reference(object):
    def __init__(
        self,
        name: str,
        application_uuid: str,
        entity_uuid: str,
        *,
        attribute: str = "uuid",
        title=None,
        metadata=None,
    ):
        self.name = name
        self.application_uuid = application_uuid
        self.entity_uuid = entity_uuid
        self.attribute = attribute
        self.title = title
        self.metadata = metadata or {}

    def collection(self, request):
        apps = request.get_collection("morpcc.application")
        app = apps.get(self.application_uuid)
        entities = request.get_collection("morpcc.entity")
        entity = entities.get(self.entity_uuid)
        return content_collection_factory(entity, app)

    def get_title(self, request):
        entities = request.get_collection("morpcc.entity")
        entity = entities.get(self.entity_uuid)
        return self.title or entity["title"]


class BackReference(object):
    def __init__(
        self,
        name: str,
        application_uuid: str,
        entity_uuid: str,
        reference_name: str,
        *,
        title=None,
        single=False,
        metadata=None,
    ):
        self.name = name
        self.application_uuid = application_uuid
        self.entity_uuid = entity_uuid
        self.reference_name = reference_name
        self.title = title
        self.single_reference = single
        self.metadata = metadata or {}

    def collection(self, request):
        apps = request.get_collection("morpcc.application")
        app = apps.get(self.application_uuid)
        entities = request.get_collection("morpcc.entity")
        entity = entities.get(self.entity_uuid)
        return content_collection_factory(entity, app)

    def get_title(self, request):
        entities = request.get_collection("morpcc.entity")
        entity = entities.get(self.entity_uuid)
        return self.title or entity["title"]

    def get_reference(self, request):
        entities = request.get_collection("morpcc.entity")
        entity = entities.get(self.entity_uuid)
        rels = entity.relationships()
        rel = rels[self.reference_name]
        return Reference(
            rel["name"],
            self.application_uuid,
            rel.reference_entity()["uuid"],
            attribute=rel.reference_attribute()["name"],
            title=rel["title"],
        )

