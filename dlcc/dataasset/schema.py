import morpfw
import jsonobject


class DataAssetSchema(morpfw.Schema):

    title = jsonobject.StringProperty()
    description = jsonobject.StringProperty()
    location = jsonobject.StringProperty()
