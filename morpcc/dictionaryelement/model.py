import morpfw

from .schema import DictionaryElementSchema


class DictionaryElementModel(morpfw.Model):
    schema = DictionaryElementSchema

    def validators(self):
        col = self.request.get_collection("morpcc.dictionaryelementvalidatorassignment")
        assignments = col.search(rulez.field["dictionaryelement_uuid"] == self.uuid)
        validators = [a.validator() for a in assignments]
        return validators


class DictionaryElementCollection(morpfw.Collection):
    schema = DictionaryElementSchema
