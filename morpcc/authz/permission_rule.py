import morepath
import rulez
from morpcc.crud.model import CollectionUI, ModelUI
from morpfw.authn.pas import permission as authnperm
from morpfw.authn.pas.user.model import UserCollection
from morpfw.authz.pas import DefaultAuthzPolicy
from morpfw.permission import All

from .policy import MorpCCAuthzPolicy

Policy = MorpCCAuthzPolicy


def rule_from_config(request, key, default=True):
    app = request.app
    value = app.get_config(key, default)
    return value


def rule_from_assignment(request, model, permission, identity):
    usercol = request.get_collection("morpfw.pas.user")
    user = usercol.get_by_userid(identity.userid)
    if user["is_administrator"]:
        return True
    pcol = request.get_collection("morpcc.permissionassignment")

    model_hierarchy = []
    for klass in model.__class__.__mro__:
        model_name = "%s:%s" % (klass.__module__, klass.__name__)
        model_hierarchy.append(model_name)

    permission_name = "%s:%s" % (permission.__module__, permission.__name__,)
    groups = user.groups()
    for model_name in model_hierarchy:
        for perm in pcol.search(
            rulez.and_(
                rulez.field["model"] == model_name,
                rulez.field["permission"] == permission_name,
            )
        ):
            if user.userid in perm["users"]:
                return True
            for g in groups:
                if g["groupname"] in perm["groups"]:
                    return True
    return False


@Policy.permission_rule(model=UserCollection, permission=authnperm.Register)
def allow_api_registration(identity, model, permission):
    return rule_from_config(model.request, "morpcc.allow_registration")


@Policy.permission_rule(model=CollectionUI, permission=All)
def collectionui_permission(identity, model, permission):
    return rule_from_assignment(model.request, model, permission, identity)


@Policy.permission_rule(model=ModelUI, permission=All)
def modelui_permission(identity, model, permission):
    return rule_from_assignment(model.request, model, permission, identity)
