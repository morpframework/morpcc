import rulez
from morpcc.crud.view.listing import listing as default_listing
from morpfw.crud import permission as crudperms
from ..app import App
from .modelui import DictionaryEntityCollectionUI

@App.html(
    model=DictionaryEntityCollectionUI,
    name="listing",
    template="master/dictionaryentity/listing.pt",
    permission=crudperms.Search,
)
def view(context, request):
    return default_listing(context, request)


