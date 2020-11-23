from ..app import App
from ..application.path import get_model as get_application
from ..entitycontent.model import content_collection_factory
from .path import get_model as get_entity


@App.indexresolver("morpcc.entity.content")
def resolve(context, request):
    app = get_application(request, context["application_uuid"])
    if not app:
        return
    dm = get_entity(request, context["entity_uuid"])
    if not dm:
        return
    col = content_collection_factory(dm, app)
    return col.get(context["entity_content_uuid"])
