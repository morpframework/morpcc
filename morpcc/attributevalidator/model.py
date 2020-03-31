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

    def ui(self):
        return AttributeValidatorModelUI(self.request, self, self.collection.ui())

    @morpfw.memoize()
    def bytecode(self):
        bytecode = compile_restricted(
            self["code"],
            filename="<AttributeValidator {}>".format(self["name"]),
            mode="exec",
        )
        return bytecode

    @morpfw.memoize()
    def function(self):
        function = get_restricted_function(
            self.request.app, self.bytecode(), "validate"
        )
        return function

    def field_validator(self):
        return AttributeValidatorWrapper(self.function(), self["error_message"])


class AttributeValidatorCollection(morpfw.Collection):
    schema = AttributeValidatorSchema

    def ui(self):
        return AttributeValidatorCollectionUI(self.request, self)
