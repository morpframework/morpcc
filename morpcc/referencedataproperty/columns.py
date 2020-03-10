from ..app import App
from .model import ReferenceDataPropertyModel


@App.structure_column(model=ReferenceDataPropertyModel, name="buttons")
def get_buttons_column(model, request, name):
    results = ""
    uiobj = model.ui()
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
