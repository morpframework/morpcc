import html

from morpfw.crud.model import Model

from ..app import App


@App.structure_column(model=Model, name="type")
def get_type_column(model, request, name):
    return str(model.__class__.__name__)


@App.structure_column(model=Model, name="object_string")
def get_objectstring_column(model, request, name):
    return html.escape(str(model))


@App.structure_column(model=Model, name="buttons")
def get_buttons_column(model, request, name):
    results = ""
    typeinfos = request.app.config.type_registry.get_typeinfos(request)
    uiobj = None
    # FIXME: have a nicer API through typeregistry
    if getattr(model, "ui", None):
        uiobj = model.ui()
    else:
        for n, ti in typeinfos.items():
            path_model = getattr(model, "__path_model__", None)
            if model.__class__ == ti["model"] or path_model == ti["model"]:
                uiobj = ti["model_ui"](
                    request, model, ti["collection_ui_factory"](request)
                )
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
