from .path import get_model as get_entity
from ..app import App

@App.indexresolver('morpcc.entity.content')
def resolve(context, request):
    dm = get_entity(request, context['entity_uuid'])
    col = dm.content_collection()
    return col.get(context['entity_content_uuid'])
