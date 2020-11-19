from ..app import App
from .model import ReferenceDataModel


@App.structure_column(model=ReferenceDataModel, name="buttons")
def get_buttons_column(model, request, name):
    uiobj = model.ui()

    buttons = [
        {
            "icon": "eye",
            "data-url": request.relative_url(
                "/referencedatakey/+datatable.json?filter=referencedata_uuid%3D%3D'{}'".format(
                    model.uuid
                )
            ),
            "data-create-url": request.relative_url(
                "/referencedatakey/+modal-create?referencedata_uuid={}".format(
                    model.uuid
                )
            ),
            "title": "View",
            "class": "refdata-view-link",
        },
        {
            "icon": "download",
            "url": request.link(uiobj, "+export"),
            "title": "Download",
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
