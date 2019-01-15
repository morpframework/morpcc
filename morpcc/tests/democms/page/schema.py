import morpfw
import jsonobject


class PageSchema(morpfw.Schema):

    title = jsonobject.StringProperty()
    description = jsonobject.StringProperty()
    location = jsonobject.StringProperty()
    body = jsonobject.StringProperty()
