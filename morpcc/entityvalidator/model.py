from RestrictedPython import compile_restricted

import morpfw
from morpcc.crud.model import CollectionUI, ModelUI
from morpfw.crud.model import Collection, Model

from ..entitycontent.model import EntityContentCollection, EntityContentModel
from ..entitycontent.modelui import EntityContentCollectionUI, EntityContentModelUI
from ..restrictedpython import get_restricted_function
from .modelui import EntityValidatorCollectionUI, EntityValidatorModelUI
from .schema import EntityValidatorSchema


class EntityValidatorWrapper(object):

    __required_binds__ = ["context"]

    def __init__(self, validator, message):
        self.validator = validator
        self.message = message

    def __call__(self, request, schema, data, mode=None, context=None):
        # FIXME: this should be a reg dispatch
        if isinstance(context, EntityContentModel):
            obj = context.validation_dict()
        elif isinstance(context, EntityContentModelUI):
            obj = context.model.validation_dict()
        elif isinstance(context, EntityContentCollection):
            obj = context.validation_dict(data)
        elif isinstance(context, EntityContentCollectionUI):
            obj = context.collection.validation_dict(data)
        else:
            raise AssertionError("Unsupported context %s" % context)

        if not self.validator(obj):
            return {"message": self.message}


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
        restricted = self.app.get_config("morpcc.pythoncompiler.restricted", True)
        if not restricted:
            return self.unrestricted_function()
        function = get_restricted_function(
            self.request.app, self.bytecode(), "validate"
        )
        return function

    def unrestricted_function(self):
        bytecode = compile(
            self["code"],
            filename="<EntityValidator {}>".format(self["name"]),
            mode="exec",
        )
        name = "validate"
        local_vars = {}
        exec(bytecode, {}, local_vars)
        func = local_vars[name]
        del local_vars[name]
        func.__globals__.update(local_vars)
        return func

    def schema_validator(self):
        return EntityValidatorWrapper(self.function(), self["error_message"])


class EntityValidatorCollection(morpfw.Collection):
    schema = EntityValidatorSchema

    def ui(self):
        return EntityValidatorCollectionUI(self.request, self)
