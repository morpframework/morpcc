from datetime import datetime

import pytz
from morpfw.crud import permission as crudperms

from ..app import App
from ..crud.view.view import view as default_view
from .modelui import NotificationModelUI


@App.html(
    model=NotificationModelUI,
    name="view",
    template="master/crud/view.pt",
    permission=crudperms.View,
)
def view(context, request):
    if not context["read"]:
        context.model.update(
            {"read": datetime.now(tz=request.timezone())}, deserialize=False
        )
    return default_view(context, request)
