import importlib
from collections import OrderedDict
from time import time

import morepath
import rulez
from morpfw.authn.pas import permission as authperm
from morpfw.authn.pas.user.model import UserCollection
from morpfw.authz.pas import APIKeyModel, CurrentUserModel, UserModel
from morpfw.crud import permission as crudperms
from morpfw.crud.model import Collection, Model
from morpfw.permission import All

from ..crud.model import CollectionUI, ModelUI
from ..util import permits
from .policy import MorpCCAuthzPolicy

Policy = MorpCCAuthzPolicy


def rule_from_config(request, key, default=True):
    app = request.app
    value = app.get_config(key, default)
    return value


def eval_config_grouppermissions(request, model, permission, identity):
    usercol = request.get_collection("morpfw.pas.user")
    user = usercol.get_by_userid(identity.userid)
    config = request.app.get_config("morpcc.authz.group_permissions", {})
    for g in user.groups():
        group_conf = config.get(g["groupname"], {})
        if not group_conf:
            continue

        model_conf = None
        for model_name in group_conf.keys():
            model_klass = import_name(model_name)
            if isinstance(model, model_klass):
                model_conf = group_conf[model_name]
                break

        if not model_conf:
            continue

        for permission_name in model_conf.keys():
            perm_klass = import_name(permission_name)
            if issubclass(permission, perm_klass) or permission == perm_klass:
                return model_conf[permission_name]
    return None


def import_name(name):
    modname, objname = name.split(":")
    mod = importlib.import_module(modname)
    return getattr(mod, objname)


def eval_permissions(request, model, permission, permissions, identity):
    usercol = request.get_collection("morpfw.pas.user")
    user = usercol.get_by_userid(identity.userid)

    user_roles = []
    for gid, roles in user.group_roles().items():
        for role in roles:
            role_ref = "%s::%s" % (gid, role)
            user_roles.append(role_ref)

    if isinstance(model, Model):
        is_creator = model["creator"] == identity.userid
    else:
        is_creator = False
    for perm in sorted(permissions, key=lambda x: 0 if x["rule"] == "reject" else 1):
        if not perm.match(model):
            continue
        perm_klass = perm.permission_class()

        if (not issubclass(permission, perm_klass)) and (
            not (permission == perm_klass)
        ):
            continue

        if is_creator and perm["is_creator"]:
            if perm["rule"] == "allow":
                return True
            else:
                return False

        if identity.userid in (perm["users"] or []):
            if perm["rule"] == "allow":
                return True
            else:
                return False

        for g in user.groups():
            if g.uuid in (perm["groups"] or []):
                if perm["rule"] == "allow":
                    return True
                else:
                    return False

        for role in user_roles:
            if role in (perm["roles"] or []):
                if perm["rule"] == "allow":
                    return True
                return False

    pass


def rule_from_assignment(request, model, permission, identity):
    usercol = request.get_collection("morpfw.pas.user")
    user = usercol.get_by_userid(identity.userid)
    if user["is_administrator"]:
        return True

    config_perm = eval_config_grouppermissions(request, model, permission, identity)
    if config_perm is not None:
        return config_perm

    # looking up permission from permission assignment is expensive. cache!
    cache = request.cache.get_cache("morpcc.permission_rule", expire=3600)
    permission_name = "%s:%s" % (permission.__module__, permission.__name__,)
    model_name = "%s:%s" % (model.__class__.__module__, model.__class__.__name__)
    if isinstance(model, Model):
        cache_key = str([identity.userid, model_name, model.uuid, permission_name,])
    else:
        cache_key = str([identity.userid, model_name, permission_name])

    def create():
        ret = _rule_from_assignment(request, model, permission, identity)
        return ret

    return cache.get(cache_key, createfunc=create)
    # return create()


def _rule_from_assignment(request, model, permission, identity):

    pcol = request.get_collection("morpcc.permissionassignment")

    resolved = request.app.resolve_permissionassignment(
        request, model, permission, identity
    )
    if resolved is not None:
        return resolved

    # find global/site permission
    res = eval_permissions(request, model, permission, pcol.all_enabled(), identity)
    if res is not None:
        return res

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
