from ..app import App
from .model import NotificationCollection
from .model import NotificationModel
from .schema import NotificationSchema
from .path import get_collection, get_model
#
from .modelui import NotificationCollectionUI
from .modelui import NotificationModelUI
from .path import get_collection_ui, get_model_ui
#


@App.typeinfo(name='morpcc.notification', schema=NotificationSchema)
def get_typeinfo(request):
    return {
        'title': 'Notification',
        'description': 'Notification type',
        'schema': NotificationSchema,
        'collection': NotificationCollection,
        'collection_factory': get_collection,
        'model': NotificationModel,
        'model_factory': get_model,
        'internal': True,
        #
        'collection_ui': NotificationCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': NotificationModelUI,
        'model_ui_factory': get_model_ui,
        #
    }
