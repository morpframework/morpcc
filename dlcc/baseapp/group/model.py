from ..crud.model import ModelUI, CollectionUI


class GroupModelUI(ModelUI):
    pass


class GroupCollectionUI(CollectionUI):

    modelui_class = GroupModelUI

    columns = [
        {'title': 'Group Name', 'name': 'groupname'},
        {'title': 'Actions', 'name': 'structure:buttons'}
    ]
