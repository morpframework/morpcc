import json

import deform
import morpfw
from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from ..app import App
from .modelui import EntityCollectionUI, EntityModelUI


@App.html(
    model=EntityModelUI,
    name="edit",
    template="master/entity/edit.pt",
    permission=crudperm.Edit,
)
def edit(context, request):
    return default_edit(context, request)


# 	@App.html(
# 	    model=EntityModelUI,
# 	    name="view",
# 	    template="master/entity/view.pt",
# 	    permission=crudperm.View,
# 	)
# 	def view(context, request):
# 	    result = default_view(context, request)
# 	    # list down columns
# 	    return result
#
