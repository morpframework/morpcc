from morpfw.crud.model import Model
from ..app import App
import html


@App.structure_column(model=Model, name='type')
def get_type_column(model, request, name):
    return str(model.__class__.__name__)


@App.structure_column(model=Model, name='object_string')
def get_objectstring_column(model, request, name):
    return html.escape(str(model))


@App.structure_column(model=Model, name='buttons')
def get_buttons_column(model, request, name):
    results = ''
    typeinfos = request.app.config.type_registry.get_typeinfos(request)
    uiobj = None
    # FIXME: have a nicer API through typeregistry
    for n, ti in typeinfos.items():
        if model.__class__ == ti['model']:
            uiobj = ti['model_ui'](request, model,
                                   ti['collection_ui_factory'](request))
            break
    if uiobj is None:
        raise ValueError('Unable to locate typeinfo for %s' % model)

    buttons = [{
        'icon': 'eye',
        'url': request.link(uiobj, '+%s' % uiobj.default_view),
        'title': 'View'
    }, {
        'icon': 'edit',
        'url': request.link(uiobj, '+edit'),
        'title': 'Edit'
    }, {
        'icon': 'trash',
        'url': request.link(uiobj, '+delete'),
        'title': 'Delete'
    }]
    for button in buttons:
        results += ('<a title="%(title)s" href="%(url)s">'
                    '<i class="fa fa-%(icon)s">'
                    '</i></a> ') % button
    return results
