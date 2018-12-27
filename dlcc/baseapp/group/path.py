from .model import GroupModelUI, GroupCollectionUI
from ..app import App
from morpfw.auth.group.path import get_group, get_group_collection


@App.path(model=GroupCollectionUI, path='/manage-groups')
def get_group_collection_ui(request):
    authapp = request.app.get_authnz_provider()
    authapp.root = request.app
    newreq = request.copy(app=authapp)
    col = get_group_collection(newreq)
    return GroupCollectionUI(newreq, col)


@App.path(model=GroupModelUI, path='/manage-groups/{groupname}',
          variables=lambda obj: {'groupname': obj.model.data['groupname']})
def get_group_model_ui(request, groupname):
    authapp = request.app.get_authnz_provider()
    authapp.root = request.app
    newreq = request.copy(app=authapp)
    group = get_group(newreq, groupname)
    return GroupModelUI(newreq, group)
