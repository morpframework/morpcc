from ..app import App
from .model import EndpointModel


@App.structure_column(model=EndpointModel, name="buttons")
def get_buttons_column(model, request, name):
    uiobj = model.ui()

    buttons = [
        {
            "icon": "eye",
            "data-url": request.relative_url(
                "/endpointhandler/+datatable.json?filter=endpoint_uuid%3D%3D'{}'".format(
                    model.uuid
                )
            ),
            "data-create-url": request.relative_url(
                "/endpointhandler/+modal-create?endpoint_uuid={}".format(model.uuid)
            ),
            "title": "View",
            "class": "endpoint-view-link",
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
