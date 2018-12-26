from ..root import ModelUI, CollectionUI


class UserModelUI(ModelUI):
    pass


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
