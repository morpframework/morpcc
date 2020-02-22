import morpfw.crud.signals as signals

from ..app import App
from ..entity.model import EntityContentModel


@App.subscribe(model=EntityContentModel, signal=signals.OBJECT_CREATED)
def index_on_create(app, request, context, signal):
    context.entity().application().index_sync(context)


@App.subscribe(model=EntityContentModel, signal=signals.OBJECT_UPDATED)
def index_on_update(app, request, context, signal):
    context.entity().application().index_sync(context)


@App.subscribe(model=EntityContentModel, signal=signals.OBJECT_TOBEDELETED)
def unindex_on_delete(app, request, context, signal):
    context.entity().application().unindex(context)
