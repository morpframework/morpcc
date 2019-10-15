from .model import GroupModelUI, GroupCollectionUI
from ..app import App
from morpfw.authn.pas.group.path import get_group, get_group_collection


@App.path(model=GroupCollectionUI, path='/manage-groups')
def get_group_collection_ui(request):
    col = get_group_collection(request)
    return GroupCollectionUI(request, col)


@App.path(model=GroupModelUI, path='/manage-groups/{groupname}',
          variables=lambda obj: {'groupname': obj.model.data['groupname']})
def get_group_model_ui(request, groupname):
    col = get_group_collection(request)
    group = get_group(request, groupname)
    return GroupModelUI(request, group, GroupCollectionUI(request, col))
