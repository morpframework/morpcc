from morpcc.crud.columns import get_buttons_column as default_get_buttons_column

from ..app import App
from .model import DataModelContentModel, DataModelModel
from .modelui import DataModelContentModelUI
from .path import get_model_content_collection_ui


@App.structure_column(model=DataModelContentModel, name="buttons")
def get_content_buttons_column(model, request, name):
    results = ""
    typeinfos = request.app.config.type_registry.get_typeinfos(request)
    uiobj = None
    # FIXME: have a nicer API through typeregistry
    uiobj = DataModelContentModelUI(
        request,
        model,
        get_model_content_collection_ui(
            request, model.collection.__parent__.identifier
        ),
    )

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


@App.structure_column(model=DataModelModel, name="buttons")
def get_buttons_column(model, request, name):
    results = ""
    typeinfos = request.app.config.type_registry.get_typeinfos(request)
    uiobj = None
    for n, ti in typeinfos.items():
        if model.__class__ == ti["model"]:
            uiobj = ti["model_ui"](request, model, ti["collection_ui_factory"](request))
            break
    if uiobj is None:
        raise ValueError("Unable to locate typeinfo for %s" % model)

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
