import morpfw
from .schema import PageSchema


class PageModel(morpfw.Model):
    schema = PageSchema

    blob_fields = ['attachment1', 'attachment2']


class PageCollection(morpfw.Collection):
    schema = PageSchema
