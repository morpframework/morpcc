import morpfw
from RestrictedPython import compile_restricted

from ..restrictedpython import get_restricted_function
from .modelui import AttributeValidatorCollectionUI, AttributeValidatorModelUI
from .schema import AttributeValidatorSchema


class AttributeValidatorWrapper(object):
    def __init__(self, validator, message):
        self.validator = validator
        self.message = message

    def __call__(self, request, schema, field, value, mode=None):
        if not self.validator(value):
            return self.message


class AttributeValidatorModel(morpfw.Model):
    schema = AttributeValidatorSchema

    bytecode_cache: dict = {}
    function_cache: dict = {}

    def ui(self):
        return AttributeValidatorModelUI(self.request, self, self.collection.ui())

    def bytecode(self):
        cache = self.bytecode_cache.get(self.uuid, None)
        if cache and cache["modified"] < self["modified"]:
            return cache["bytecode"]
        bytecode = compile_restricted(
            self["code"],
            filename="<AttributeValidator {}>".format(self["name"]),
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

    def field_validator(self):
        return AttributeValidatorWrapper(self.function(), self["error_message"])


class AttributeValidatorCollection(morpfw.Collection):
    schema = AttributeValidatorSchema

    def ui(self):
        return AttributeValidatorCollectionUI(self.request, self)
