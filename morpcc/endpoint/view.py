import os
import traceback

from morpfw.crud import permission as crudperm
from morpfw.crud.errors import ValidationError
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
from RestrictedPython.Guards import (
    full_write_guard,
    guarded_iter_unpack_sequence,
    safer_getattr,
)

from ..app import App
from .model import EndpointModel
from .modelui import EndpointModelUI
from .restrictedcontext import RestrictedContext, RestrictedRequest


def default_inplacevar(op, x, y):
    if op == "+=":
        return x + y
    raise Exception("{} operator is not allowed".format(op))


BYTECODE_CACHE = {}


def _handle(context, request):
    code = context["code"]
    cache = BYTECODE_CACHE.get(context.uuid, None)
    if cache is None or cache["modified"] < context["modified"]:
        try:
            bytecode = compile_restricted(
                code, filename="<include code {}>".format(context["name"]), mode="exec"
            )
        except Exception:

            @request.after
            def set_code(response):
                response.status_code = 500

            tb = traceback.format_exc().split("\n")
            return {"status": "error", "traceback": tb}

        cache = {"bytecode": bytecode, "modified": context["modified"]}
        BYTECODE_CACHE[context.uuid] = cache

    bytecode = cache["bytecode"]
    loc = {}
    glob = safe_globals.copy()
    glob["dir"] = dir
    glob["_getiter_"] = default_guarded_getiter
    glob["_getitem_"] = default_guarded_getitem
    glob["_iter_unpack_sequence_"] = guarded_iter_unpack_sequence
    glob["_write_"] = full_write_guard
    glob["_inplacevar_"] = default_inplacevar
    glob["getattr"] = safer_getattr
    glob["enumerate"] = enumerate
    ctx = RestrictedContext(context, request)
    req = RestrictedRequest(request)
    try:
        exec(bytecode, glob, loc)
        return loc["handle"](ctx, req)
    except ValidationError as e:
        raise e
    except Exception:

        @request.after
        def set_code(response):
            response.status_code = 500

        tb = traceback.format_exc().split("\n")
        return {"status": "error", "traceback": tb}


@App.json(model=EndpointModel, name="handle", permission=crudperm.View)
def handle_GET(context, request):
    return _handle(context, request)


@App.json(
    model=EndpointModel, name="handle", permission=crudperm.View, request_method="POST"
)
def handle_POST(context, request):
    return _handle(context, request)
