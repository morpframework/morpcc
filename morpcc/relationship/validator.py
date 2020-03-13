import rulez


class EntityContentReferenceValidator(object):
    def __init__(self, application_uuid, entity_uuid, attribute):
        self.application_uuid = application_uuid
        self.entity_uuid = entity_uuid
        self.attribute = attribute

    def __call__(self, request, schema, field, value, mode=None):
        resource = self.get_resource(request, value)
        if not resource:
            return "Invalid reference : {}".format(value)

    def get_resource(self, request, identifier):
        from ..entitycontent.path import get_content_collection

        col = get_content_collection(request, self.application_uuid, self.entity_uuid)
        models = col.search(rulez.field[self.attribute] == identifier)
        if models:
            return models[0]
        return None
