import rulez
from colander import Invalid, null
from deform.compat import string_types
from deform.widget import SelectWidget, Widget


class EntityContentReferenceWidget(SelectWidget):
    template = "reference"
    readonly_template = "readonly/reference"
    null_value = ""
    values = ()
    multiple = False

    def __init__(self, entity_uuid, term_field, value_field, **kwargs):
        self.entity_uuid = entity_uuid
        self.term_field = term_field
        self.value_field = value_field
        super().__init__(**kwargs)

    def get_resource_search_url(self, context, request):
        from ..entity.modelui import EntityModelUI, EntityCollectionUI
        from ..entity.path import get_model as get_entity
        entity = get_entity(request, self.entity_uuid)
        colui = EntityCollectionUI(request, entity.collection)
        mui = EntityModelUI(request, entity, colui)
        baselink = request.link(mui, "+term-search")

        return baselink + "?term_field=%s&value_field=%s" % (
            self.term_field,
            self.value_field,
        )

    def get_resource_url(self, request, identifier):
        m = self.get_resource(request, identifier)
        if not m:
            return None
        return request.link(m)

    def get_resource(self, request, identifier):
        from ..entity.path import _get_model_content_collection_ui
        from ..entity.path import get_model as get_entity

        entity = get_entity(request, self.entity_uuid)

        col = _get_model_content_collection_ui(entity, request)
        res = col.search(rulez.field[self.value_field] == identifier)
        if res:
            return res[0]
        return None

    def get_resource_term(self, request, identifier):
        m = self.get_resource(request, identifier)
        if not m:
            return None
        return m.model[self.term_field]
