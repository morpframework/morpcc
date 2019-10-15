import os
from morpfw.authn.pas.user.model import UserModel
from morpfw.crud.blobstorage.fsblobstorage import FSBlobStorage
from ..app import App
from ..crud.model import ModelUI, CollectionUI


@App.blobstorage(model=UserModel)
def get_user_blobstorage(model, request):
    return FSBlobStorage(request, request.app.settings.application.fsblobstorage_path % {'here': os.getcwd()})


class UserModelUI(ModelUI):

    view_exclude_fields = ModelUI.view_exclude_fields + ['password', 'nonce']
    edit_include_fields = ['email']


class UserCollectionUI(CollectionUI):

    modelui_class = UserModelUI

    page_title = 'Users'
    listing_title = 'Registered Users'

    columns = [
        {'title': 'Username', 'name': 'username'},
        {'title': 'Created', 'name': 'created'},
        {'title': 'State', 'name': 'state'},
        {'title': 'Actions', 'name': 'structure:buttons'},
    ]


class CurrentUserModelUI(UserModelUI):
    pass
