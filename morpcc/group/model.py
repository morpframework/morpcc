from ..crud.model import ModelUI, CollectionUI


class GroupModelUI(ModelUI):

    edit_include_fields = ['groupname']


class GroupCollectionUI(CollectionUI):

    modelui_class = GroupModelUI

    create_include_fields = ['groupname']

    columns = [
        {'title': 'Group Name', 'name': 'groupname'},
        {'title': 'Actions', 'name': 'structure:buttons'}
    ]
