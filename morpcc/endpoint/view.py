import os
import traceback

import rulez
from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm
from morpfw.crud.errors import ValidationError
from RestrictedPython import compile_restricted
from webob.exc import HTTPNotFound

from ..app import App
from ..endpointhandler.schema import ALLOWED_METHODS
from ..restrictedpython import get_restricted_function
from .model import EndpointCollectionUI, EndpointModel, NamedEndpointModel
from .modelui import EndpointModelUI
from .restrictedcontext import RestrictedContext, RestrictedRequest


@App.html(
    model=EndpointCollectionUI,
    name="listing",
    template="master/endpoint/listing.pt",
    permission=crudperm.Search,
)
def view(context, request):
    return default_listing(context, request)


def _handle(context, request):
    hcol = request.get_collection("morpcc.endpointhandler")
    handlers = hcol.search(
        rulez.and_(
            rulez.field["endpoint_uuid"] == context.uuid,
            rulez.field["method"] == request.method,
        )
    )
    if not handlers:
        raise HTTPNotFound()
    handler = handlers[0].function()
    ctx = RestrictedContext(request)
    req = RestrictedRequest(request)
    return handler(ctx, req)


for method in ALLOWED_METHODS:

    App.json(
        model=EndpointModel,
        name="handle",
        permission=crudperm.View,
        request_method=method,
    )(_handle)
    App.json(model=NamedEndpointModel, permission=crudperm.View, request_method=method)(
        _handle
    )
