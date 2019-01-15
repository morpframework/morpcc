from ..app import App
from .model import UserModelUI
from morpfw.crud import permission as crudperms


@App.html(model=UserModelUI, permission=crudperms.View, template='auth/user.pt')
def view(context, request):
    return {}
