import morepath
import html
import deform
from morpfw.crud import permission as crudperms
from ..model import CollectionUI, ModelUI
from ...app import App
from ...util import dataclass_to_colander
import rulez


def _term_search(context, request):
    resource_type = request.GET.get('resource_type', '').strip()
    if not resource_type:
        return {}
    value_field = request.GET.get('value_field', '').strip()
    if not value_field:
        return {}
    term_field = request.GET.get('term_field', '').strip()
    if not term_field:
        return {}
    term = request.GET.get('term', '').strip()
    if not term:
        return {}

    typeinfo = request.app.config.type_registry.get_typeinfo(
        name=resource_type, request=request)
    col = typeinfo['collection_factory'](request)
    objs = col.search(query={
        'field': term_field,
        'operator': '~',
        'value': term
    })
    result = {
        'results': []
    }
    for obj in objs:
        result['results'].append({
            'id': obj[value_field],
            'text': obj[term_field]
        })
    return result


@App.json(model=ModelUI, name='term-search')
def model_term_search(context, request):
    return _term_search(context, request)


@App.json(model=CollectionUI, name='term-search')
def collection_term_search(context, request):
    return _term_search(context, request)
