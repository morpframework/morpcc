import morepath
import rulez
from morpfw.authn.pas import permission as authperm
from morpfw.authn.pas.user.model import UserCollection
from morpfw.authz.pas import APIKeyModel, CurrentUserModel, UserModel
from morpfw.crud import permission as crudperms
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
    epcol = request.get_collection("morpcc.entitypermissionassignment")

    permission_name = "%s:%s" % (permission.__module__, permission.__name__,)
    groups = user.groups()

    user_roles = []
    for gid, roles in user.group_roles().items():
        for role in roles:
            role_ref = "%s::%s" % (gid, role)
            user_roles.append(role_ref)

    # find object permission
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

    # find entity model permission
    if isinstance(model, EntityContentModel) or isinstance(model, EntityContentModelUI):
        found_perms = []
        if isinstance(model, EntityContentModel):
            ec = model.collection
        elif isinstance(model, EntityContentModelUI):
            ec = model.model.collection
        else:
            # shouldnt reach here, but assert if hit
            raise AssertionError("Invalid model type")
        ecapp = ec.application()
        ecent = ec.entity()
        for perm in epcol.search(
            rulez.and_(
                rulez.field["application_uuid"] == ecapp.uuid,
                rulez.field["entity_uuid"] == ecent.uuid,
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

    # find entity collection permission
    if isinstance(model, EntityContentCollection) or isinstance(
        model, EntityContentCollectionUI
    ):
        found_perms = []
        if isinstance(model, EntityContentCollection):
            ec = model
        elif isinstance(model, EntityContentCollectionUI):
            ec = model.collection
        else:
            # shouldnt reach here, but assert if hit
            raise AssertionError("Invalid model type")
        ecapp = ec.application()
        ecent = ec.entity()
        for perm in epcol.search(
            rulez.and_(
                rulez.field["application_uuid"] == ecapp.uuid,
                rulez.field["entity_uuid"] == ecent.uuid,
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

    # find application permission
    if (
        isinstance(model, EntityContentCollection)
        or isinstance(model, EntityContentCollectionUI)
        or isinstance(model, EntityContentModel)
        or isinstance(model, EntityContentModelUI)
    ):
        found_perms = []
        if isinstance(model, EntityContentCollection):
            ec = model
        elif isinstance(model, EntityContentCollectionUI):
            ec = model.collection
        elif isinstance(model, EntityContentModel):
            ec = model.collection
        elif isinstance(model, EntityContentModelUI):
            ec = model.model.collection
        else:
            # shouldnt reach here, but assert if hit
            raise AssertionError("Invalid model type")
        ecapp = ec.application()
        ecent = ec.entity()
        for perm in opcol.search(
            rulez.and_(
                rulez.field["object_uuid"] == ecapp.uuid,
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

    # find global/site permission
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


@Policy.permission_rule(model=UserCollection, permission=authperm.Register)
def allow_api_registration(identity, model, permission):
    return model.request.app.get_config("morpfw.new_registration.enabled", True)


@Policy.permission_rule(model=Collection, permission=All)
def collection_permission(identity, model, permission):
    return rule_from_assignment(model.request, model, permission, identity)


@Policy.permission_rule(model=CollectionUI, permission=All)
def collectionui_permission(identity, model, permission):
    return permits(model.request, model.collection, permission)


@Policy.permission_rule(model=ModelUI, permission=All)
def modelui_permission(identity, model, permission):
    return permits(model.request, model.model, permission)


@Policy.permission_rule(model=Model, permission=All)
def model_permission(identity, model, permission):
    return rule_from_assignment(model.request, model, permission, identity)


def currentuser_permission(identity, model, permission):
    request = model.request
    usercol = request.get_collection("morpfw.pas.user")
    user = usercol.get_by_userid(identity.userid)
    if user["is_administrator"]:
        return True
    userid = identity.userid
    if isinstance(model, UserModel):
        if model.userid == userid:
            return True
    elif isinstance(model, APIKeyModel):
        if model["userid"] == userid:
            return True

    return rule_from_assignment(
        request=model.request, model=model, permission=permission, identity=identity
    )


@Policy.permission_rule(model=UserModel, permission=crudperms.All)
def allow_user_crud(identity, model, permission):
    return currentuser_permission(identity, model, permission)


@Policy.permission_rule(model=UserModel, permission=authperm.ChangePassword)
def allow_change_password(identity, model, permission):
    return currentuser_permission(identity, model, permission)


@Policy.permission_rule(model=CurrentUserModel, permission=authperm.ChangePassword)
def allow_self_change_password(identity, model, permission):
    return currentuser_permission(identity, model, permission)


@Policy.permission_rule(model=APIKeyModel, permission=crudperms.All)
def allow_apikey_management(identity, model, permission):
    return currentuser_permission(identity, model, permission)
