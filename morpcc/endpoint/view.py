import os
import traceback

from morpfw.crud import permission as crudperm
from morpfw.crud.errors import ValidationError
from RestrictedPython import compile_restricted

from ..app import App
from ..restrictedpython import get_restricted_function
from .model import EndpointModel
from .modelui import EndpointModelUI
from .restrictedcontext import RestrictedContext, RestrictedRequest

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
    handler = get_restricted_function(bytecode, "handle")
    ctx = RestrictedContext(context, request)
    req = RestrictedRequest(request)
    try:
        return handler(ctx, req)
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


@App.json(
    model=EndpointModel, name="handle", permission=crudperm.View, request_method="PATCH"
)
def handle_PATCH(context, request):
    return _handle(context, request)


@App.json(
    model=EndpointModel,
    name="handle",
    permission=crudperm.View,
    request_method="DELETE",
)
def handle_DELETE(context, request):
    return _handle(context, request)
