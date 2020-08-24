from morpcc.crud.columns import \
    get_buttons_column as default_get_buttons_column
from morpcc.util import permits
from morpfw.crud import permission as crudperm

from ..app import App
from ..entitycontent.model import EntityContentModel
from ..entitycontent.modelui import EntityContentModelUI
from .model import EntityModel


@App.structure_column(model=EntityContentModel, name="buttons")
def get_content_buttons_column(model, request, name):
    uiobj = model.ui()

    buttons = []

    if permits(request, uiobj, crudperm.View):
        buttons.append(
            {
                "icon": "eye",
                "url": request.link(uiobj, "+%s" % uiobj.default_view),
                "title": "View",
            }
        )

    if permits(request, uiobj, crudperm.Edit):
        buttons.append(
            {"icon": "edit", "url": request.link(uiobj, "+edit"), "title": "Edit"}
        )

    if permits(request, uiobj, crudperm.Delete):
        buttons.append(
            {
                "icon": "trash",
                "data-url": request.link(uiobj, "+modal-delete"),
                "title": "Delete",
                "class": "modal-link",
            }
        )

    render = request.app.get_template("master/snippet/button-group-sm.pt")
    return render({"buttons": buttons}, request)


@App.structure_column(model=EntityModel, name="buttons")
def get_buttons_column(model, request, name):
    uiobj = model.ui()

    buttons = []

    if permits(request, uiobj, crudperm.View):
        buttons.append(
            {
                "icon": "eye",
                "url": request.link(uiobj, "+%s" % uiobj.default_view),
                "title": "View",
            }
        )

    if permits(request, uiobj, crudperm.Edit):
        buttons.append(
            {"icon": "edit", "url": request.link(uiobj, "+edit"), "title": "Edit",}
        )

    if permits(request, uiobj, crudperm.Delete):
        buttons.append(
            {
                "icon": "trash",
                "data-url": request.link(uiobj, "+modal-delete"),
                "title": "Delete",
                "class": "modal-link",
            }
        )
        
    render = request.app.get_template("master/snippet/button-group-sm.pt")
    return render({"buttons": buttons}, request)
