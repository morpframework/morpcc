import morpfw
from RestrictedPython import compile_restricted

from .. import log
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
        restricted = self.app.get_config("morpcc.pythoncompiler.restricted", True)
        if not restricted:
            return self.unrestricted_function()
        function = get_restricted_function(
            self.request.app, self.bytecode(), "validate"
        )
        return function

    def unrestricted_function(self):
        log.warn("Unrestricted function compiler is insecure")
        bytecode = compile(
            self["code"],
            filename="<AttributeValidator {}>".format(self["name"]),
            mode="exec",
        )
        name = "validate"
        local_vars = {}
        exec(bytecode, {}, local_vars)
        func = local_vars[name]
        del local_vars[name]
        func.__globals__.update(local_vars)
        return func

    def field_validator(self):
        return AttributeValidatorWrapper(self.function(), self["error_message"])


class AttributeValidatorCollection(morpfw.Collection):
    schema = AttributeValidatorSchema

    def ui(self):
        return AttributeValidatorCollectionUI(self.request, self)
