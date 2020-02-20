from .path import get_model as get_datamodel
from ..app import App

@App.indexresolver('morpcc.datamodel.content')
def resolve(context, request):
    dm = get_datamodel(request, context['datamodel_uuid'])
    col = dm.content_collection()
    return col.get(context['datamodel_content_uuid'])
