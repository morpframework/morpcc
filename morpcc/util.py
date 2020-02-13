import copy
import dataclasses
from dataclasses import field
from datetime import date, datetime
from importlib import import_module

from pkg_resources import resource_filename

import colander
from deform.widget import HiddenWidget
from morpfw.crud.schemaconverter.common import (dataclass_check_type,
                                                dataclass_get_type)
from morpfw.crud.schemaconverter.dataclass2colander import \
    dataclass_to_colander
from morpfw.interfaces import ISchema


def permits(request, context, permission):
    perm_mod, perm_cls = permission.split(":")
    mod = import_module(perm_mod)
    klass = getattr(mod, perm_cls)
    return request.app._permits(request.identity, context, klass)
