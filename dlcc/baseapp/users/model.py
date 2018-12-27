from ..crud.model import ModelUI, CollectionUI


class UserModelUI(ModelUI):

    view_exclude_fields = ['password', 'attrs', 'nonce']
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
