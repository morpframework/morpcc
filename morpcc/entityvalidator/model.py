import morpfw
from RestrictedPython import compile_restricted

from ..restrictedpython import get_restricted_function
from .modelui import EntityValidatorCollectionUI, EntityValidatorModelUI
from .schema import EntityValidatorSchema


class EntityValidatorWrapper(object):
    def __init__(self, validator, message):
        self.validator = validator
        self.message = message

    def __call__(self, request, data, mode=None):
        if not self.validator(data):
            return self.message


class EntityValidatorModel(morpfw.Model):
    schema = EntityValidatorSchema

    def ui(self):
        return EntityValidatorModelUI(self.request, self, self.collection.ui())

    @morpfw.memoize()
    def bytecode(self):
        bytecode = compile_restricted(
            self["code"],
            filename="<EntityValidator {}>".format(self["name"]),
            mode="exec",
        )
        return bytecode

    @morpfw.memoize()
    def function(self):
        function = get_restricted_function(self.bytecode(), "validate")
        return function

    def entity_validator(self):
        return EntityValidatorWrapper(self.function(), self["error_message"])


class EntityValidatorCollection(morpfw.Collection):
    schema = EntityValidatorSchema

    def ui(self):
        return EntityValidatorCollectionUI(self.request, self)
