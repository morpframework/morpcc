from ..app import App
from .model import ReferenceDataKeyModel


@App.structure_column(model=ReferenceDataKeyModel, name="buttons")
def get_buttons_column(model, request, name):
    uiobj = model.ui()

    buttons = [
        {
            "icon": "eye",
            "data-url": request.relative_url(
                "/referencedataproperty/+datatable.json?filter=referencedatakey_uuid%3D%3D'{}'".format(
                    model.uuid
                )
            ),
            "data-create-url": request.relative_url(
                "/referencedataproperty/+modal-create?referencedatakey_uuid={}".format(
                    model.uuid
                )
            ),
            "title": "View",
            "class": "refdatakey-view-link",
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
