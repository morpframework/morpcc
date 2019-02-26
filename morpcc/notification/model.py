import morpfw
from .schema import NotificationSchema


class NotificationModel(morpfw.Model):
    schema = NotificationSchema


class NotificationCollection(morpfw.Collection):
    schema = NotificationSchema
