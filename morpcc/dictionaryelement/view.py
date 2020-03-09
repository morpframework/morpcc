from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm

from ..app import App
from .model import DictionaryElementCollection, DictionaryElementModel
from .modelui import DictionaryElementCollectionUI, DictionaryElementModelUI


@App.html(
    model=DictionaryElementModelUI,
    name="edit",
    template="master/dictionaryelement/edit.pt",
    permission=crudperm.Edit,
)
def edit(context, request):
    return default_edit(context, request)
