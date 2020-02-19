import morpfw.crud.signals as signals

from ..app import App
from ..datamodel.model import DataModelContentModel


@App.subscribe(model=DataModelContentModel, signal=signals.OBJECT_CREATED)
def index_on_create(app, request, context, signal):
    context.datamodel().application().index_sync(context)


@App.subscribe(model=DataModelContentModel, signal=signals.OBJECT_UPDATED)
def index_on_update(app, request, context, signal):
    context.datamodel().application().index_sync(context)


@App.subscribe(model=DataModelContentModel, signal=signals.OBJECT_TOBEDELETED)
def unindex_on_delete(app, request, context, signal):
    context.datamodel().application().unindex(context)
