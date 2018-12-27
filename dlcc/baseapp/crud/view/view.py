import morepath
import html
import deform
from morpfw.crud import permission as crudperms
from ..model import CollectionUI, ModelUI
from ...app import App
from ...util import jsonobject_to_colander


@App.view(model=CollectionUI)
def collection_index(context, request):
    return morepath.redirect(request.link(context, '+%s' % context.default_view))


@App.view(model=ModelUI)
def model_index(context, request):
    return morepath.redirect(request.link(context, '+%s' % context.default_view))


@App.html(model=ModelUI, name='view', template='master/simple-form.pt', permission=crudperms.View)
def view(context, request):
    formschema = jsonobject_to_colander(
        context.model.schema,
        include_fields=context.view_include_fields,
        exclude_fields=context.view_exclude_fields)
    data = context.model.data.as_dict()
    return {
        'page_title': 'View %s' % html.escape(str(context.model.__class__.__name__)),
        'form_title': 'View',
        'form': deform.Form(formschema(), buttons=('Submit',)),
        'form_data': data,
        'readonly': True
    }
