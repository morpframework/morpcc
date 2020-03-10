from morpcc.crud.columns import get_buttons_column as default_get_buttons_column

from ..app import App
from ..entitycontent.model import EntityContentModel
from ..entitycontent.modelui import EntityContentModelUI
from .model import EntityModel


@App.structure_column(model=EntityContentModel, name="buttons")
def get_content_buttons_column(model, request, name):
    results = ""
    typeinfos = request.app.config.type_registry.get_typeinfos(request)
    uiobj = model.ui()

    buttons = [
        {
            "icon": "eye",
            "url": request.link(uiobj, "+%s" % uiobj.default_view),
            "title": "View",
        },
        {"icon": "edit", "url": request.link(uiobj, "+edit"), "title": "Edit",},
        {
            "icon": "trash",
            "data-url": request.link(uiobj, "+modal-delete"),
            "title": "Delete",
            "class": "modal-link",
        },
    ]
    for button in buttons:
        button.setdefault("class", None)
        if button.get("data-url", None):
            results += (
                '<a title="%(title)s" data-url="%(data-url)s" '
                'href="#" class="%(class)s">'
                '<i class="fa fa-%(icon)s">'
                "</i></a> "
            ) % button
        else:
            results += (
                '<a title="%(title)s" href="%(url)s" '
                'class="%(class)s"> '
                '<i class="fa fa-%(icon)s">'
                "</i></a> "
            ) % button
    return results


@App.structure_column(model=EntityModel, name="buttons")
def get_buttons_column(model, request, name):
    results = ""
    uiobj = model.ui()

    buttons = [
        {
            "icon": "eye",
            "url": request.link(uiobj, "+%s" % uiobj.default_view),
            "title": "View",
        },
        {"icon": "edit", "url": request.link(uiobj, "+edit"), "title": "Edit",},
        {
            "icon": "trash",
            "data-url": request.link(uiobj, "+modal-delete"),
            "title": "Delete",
            "class": "modal-link",
        },
    ]
    for button in buttons:
        button.setdefault("class", None)
        if button.get("data-url", None):
            results += (
                '<a title="%(title)s" data-url="%(data-url)s" '
                'href="#" class="%(class)s">'
                '<i class="fa fa-%(icon)s">'
                "</i></a> "
            ) % button
        else:
            results += (
                '<a title="%(title)s" href="%(url)s" '
                'class="%(class)s"> '
                '<i class="fa fa-%(icon)s">'
                "</i></a> "
            ) % button
    return results
