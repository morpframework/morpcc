import copy
import dataclasses
from dataclasses import field
from datetime import date, datetime
from importlib import import_module

from pkg_resources import resource_filename

import colander
from deform.widget import HiddenWidget
from inverter.common import dataclass_check_type, dataclass_get_type
from morpfw.interfaces import ISchema


def permits(request, context, permission):
    if isinstance(permission, str):
        perm_mod, perm_cls = permission.split(":")
        mod = import_module(perm_mod)
        klass = getattr(mod, perm_cls)
    else:
        klass = permission
    return request.app._permits(request.identity, context, klass)
