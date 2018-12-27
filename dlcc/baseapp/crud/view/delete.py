import morepath
import html
import deform
from morpfw.crud import permission as crudperms
from ..model import CollectionUI, ModelUI
from ...app import App
from ...util import jsonobject_to_colander


@App.html(model=ModelUI, name='delete', template='master/crud/delete.pt',
          permission=crudperms.Delete)
def delete(context, request):

    formschema = jsonobject_to_colander(
        context.model.schema,
        include_fields=context.view_include_fields,
        exclude_fields=context.view_exclude_fields)
    data = context.model.data.as_dict()
    return {
        'page_title': 'Delete Confirmation',
        'form_title': 'Are you sure you want to delete this?',
        'form': deform.Form(formschema()),
        'form_data': data
    }
