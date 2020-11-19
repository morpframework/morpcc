from ..app import App
from .model import DictionaryEntityModel


@App.structure_column(model=DictionaryEntityModel, name="buttons")
def get_buttons_column(model, request, name):
    uiobj = model.ui()

    buttons = [
        {
            "icon": "eye",
            "data-url": request.relative_url(
                "/dictionaryelement/+datatable.json?filter=dictionaryentity_uuid%3D%3D'{}'".format(
                    model.uuid
                )
            ),
            "data-create-url": request.relative_url(
                "/dictionaryelement/+modal-create?dictionaryentity_uuid={}".format(
                    model.uuid
                )
            ),
            "title": "View",
            "class": "dictionaryentity-view-link",
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
