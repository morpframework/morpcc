from ..app import App
from .modelui import AttributeModelUI
from morpcc.crud.view.edit import edit as default_edit
from morpfw.crud import permission as crudperm


@App.html(
    model=AttributeModelUI,
    name="edit",
    template="master/attribute/edit.pt",
    permission=crudperm.Edit
)
def edit(request, context):
    return default_edit(request, context)
