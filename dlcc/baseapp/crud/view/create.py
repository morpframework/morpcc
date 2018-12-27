import morepath
import html
import deform
from morpfw.crud import permission as crudperms
from ..model import CollectionUI, ModelUI
from ...app import App
from ...util import jsonobject_to_colander


@App.html(model=CollectionUI, name='create', template='master/simple-form.pt',
          permission=crudperms.Create)
def create(context, request):
    formschema = jsonobject_to_colander(
        context.collection.schema, include_fields=context.create_include_fields,
        exclude_fields=context.create_exclude_fields)
    return {
        'page_title': 'Create %s' % html.escape(
            str(context.collection.__class__.__name__.replace('Collection', ''))),
        'form_title': 'Create',
        'form': deform.Form(formschema(), buttons=('Submit',)),
    }
