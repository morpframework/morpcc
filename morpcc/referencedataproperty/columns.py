from ..app import App
from .model import ReferenceDataPropertyModel


@App.structure_column(model=ReferenceDataPropertyModel, name="buttons")
def get_buttons_column(model, request, name):
    results = ""
    typeinfos = request.app.config.type_registry.get_typeinfos(request)
    uiobj = None
    # FIXME: have a nicer API through typeregistry
    for n, ti in typeinfos.items():
        if model.__class__ == ti["model"]:
            uiobj = ti["model_ui"](request, model, ti["collection_ui_factory"](request))
            break
    if uiobj is None:
        raise ValueError("Unable to locate typeinfo for %s" % model)

    buttons = [
        {
            "icon": "eye",
            "data-url": request.link(uiobj, "+modal-view"),
            "title": "View",
            "class": "modal-link",
        },
        {
            "icon": "edit",
            "data-url": request.link(uiobj, "+modal-edit"),
            "title": "Edit",
            "class": "modal-link",
        },
        {
            "icon": "trash",
            "data-url": request.link(uiobj, "+modal-delete"),
            "title": "Delete",
            "class": "modal-link",
        },
    ]
    for button in buttons:
        results += (
            '<a title="%(title)s" class="%(class)s" data-url="%(data-url)s" href="#">'
            '<i class="fa fa-%(icon)s">'
            "</i></a> "
        ) % button
    return results
