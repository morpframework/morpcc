import morpfw
import jsonobject
from morpfw.authn.pas.user.model import UserModel
from morpfw.crud.xattrprovider import FieldXattrProvider
from ..app import App, SQLAuthApp


class UserXattrSchema(jsonobject.JsonObject):

    firstname = jsonobject.StringProperty()
    lastname = jsonobject.StringProperty()
    displayname = jsonobject.StringProperty()
    address = jsonobject.StringProperty()


class UserXattrProvider(FieldXattrProvider):

    schema = UserXattrSchema


@SQLAuthApp.xattrprovider(model=UserModel)
def get_xattr_provider(context):
    return UserXattrProvider(context)
