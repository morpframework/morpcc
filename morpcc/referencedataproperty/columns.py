from ..app import App
from .model import ReferenceDataPropertyModel


@App.structure_column(model=ReferenceDataPropertyModel, name="buttons")
def get_buttons_column(model, request, name):
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

    render = request.app.get_template("master/snippet/button-group-sm.pt")
    return render({"buttons": buttons}, request)
