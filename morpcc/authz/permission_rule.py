import morepath
import rulez
from morpfw.authn.pas import permission as authnperm
from morpfw.authn.pas.user.model import UserCollection
from morpfw.authz.pas import DefaultAuthzPolicy
from morpfw.crud.model import Collection, Model
from morpfw.permission import All

from ..crud.model import CollectionUI, ModelUI
from ..entitycontent.model import EntityContentCollection, EntityContentModel
from ..entitycontent.modelui import EntityContentCollectionUI, EntityContentModelUI
from ..util import permits
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
    opcol = request.get_collection("morpcc.objectpermissionassignment")

    permission_name = "%s:%s" % (permission.__module__, permission.__name__,)
    groups = user.groups()

    user_roles = []
    for gid, roles in user.group_roles().items():
        for role in roles:
            role_ref = "%s::%s" % (gid, role)
            user_roles.append(role_ref)

    if isinstance(model, Model) or isinstance(model, ModelUI):
        found_perms = []
        for perm in opcol.search(
            rulez.and_(
                rulez.field["object_uuid"] == model.uuid,
                rulez.field["permission"] == permission_name,
                rulez.field["enabled"] == True,
            )
        ):
            found_perms.append(perm)

        for perm in sorted(
            found_perms, key=lambda x: 0 if x["rule"] == "reject" else 1
        ):
            for role in user_roles:
                if role in (perm["roles"] or []):
                    if perm["rule"] == "allow":
                        return True
                    return False

    model_hierarchy = []
    for klass in model.__class__.__mro__:
        model_name = "%s:%s" % (klass.__module__, klass.__name__)
        model_hierarchy.append(model_name)

    for model_name in model_hierarchy:
        found_perms = []
        for perm in pcol.search(
            rulez.and_(
                rulez.field["model"] == model_name,
                rulez.field["permission"] == permission_name,
                rulez.field["enabled"] == True,
            )
        ):
            found_perms.append(perm)

        for perm in sorted(
            found_perms, key=lambda x: 0 if x["rule"] == "reject" else 1
        ):
            for role in user_roles:
                if role in (perm["roles"] or []):
                    if perm["rule"] == "allow":
                        return True
                    return False

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


@Policy.permission_rule(model=EntityContentModelUI, permission=All)
def entitycontentmodelui_permission(identity, model, permission):
    application = model.model.collection.application()
    return rule_from_assignment(model.request, application, permission, identity)


@Policy.permission_rule(model=EntityContentModel, permission=All)
def entitycontentmodel_permission(identity, model, permission):
    application = model.collection.application()
    return rule_from_assignment(model.request, application, permission, identity)


@Policy.permission_rule(model=EntityContentCollectionUI, permission=All)
def entitycontentcollectionui_permission(identity, model, permission):
    application = model.collection.application()
    return rule_from_assignment(model.request, application, permission, identity)


@Policy.permission_rule(model=EntityContentCollection, permission=All)
def entitycontentcollection_permission(identity, model, permission):
    application = model.application()
    return rule_from_assignment(model.request, application, permission, identity)
