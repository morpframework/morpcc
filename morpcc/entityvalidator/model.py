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

    bytecode_cache: dict = {}
    function_cache: dict = {}

    def ui(self):
        return EntityValidatorModelUI(self.request, self, self.collection.ui())

    def bytecode(self):
        cache = self.bytecode_cache.get(self.uuid, None)
        if cache and cache["modified"] < self["modified"]:
            return cache["bytecode"]
        bytecode = compile_restricted(
            self["code"],
            filename="<EntityValidator {}>".format(self["name"]),
            mode="exec",
        )
        self.bytecode_cache[self.uuid] = {
            "bytecode": bytecode,
            "modified": self["modified"],
        }
        return bytecode

    def function(self):
        cache = self.function_cache.get(self.uuid, None)
        if cache and cache["modified"] < self["modified"]:
            return cache["function"]
        function = get_restricted_function(self.bytecode(), "validate")
        self.function_cache[self.uuid] = {
            "function": function,
            "modified": self["modified"],
        }
        return function

    def entity_validator(self):
        return EntityValidatorWrapper(self.function(), self["error_message"])


class EntityValidatorCollection(morpfw.Collection):
    schema = EntityValidatorSchema

    def ui(self):
        return EntityValidatorCollectionUI(self.request, self)
