import typing
from dataclasses import dataclass, field

import deform.widget
import morpfw

from ..root import Root

MODELS = [Root]


def permission_select_widget(request):
    views = list(request.app.get_view.by_args.__self__.registry.known_values)
    permissions = set()
    for view in views:
        perm = view.permission
        if perm:
            name = "%s:%s" % (perm.__module__, perm.__name__)
            permissions.add((name, name))

    permissions = sorted(list(permissions), key=lambda x: x[0])
    return deform.widget.Select2Widget(values=permissions)


def model_select_widget(request):
    models = list()
    types = sorted(request.app.config.type_registry.types)
    for t in types:
        ti = request.app.get_typeinfo(t, request)
        for model in [
            ti["collection"],
            ti["model"],
            ti["collection_ui"],
            ti["model_ui"],
        ]:
            name = "%s:%s" % (model.__module__, model.__name__)
            models.append((name, name))

    for model in MODELS:
        name = "%s:%s" % (model.__module__, model.__name__)
        models.append((name, name))
    return deform.widget.Select2Widget(values=models)


def group_select_widget(request):
    groups = request.get_collection("morpfw.pas.group").all()
    choices = [(g["groupname"], g["groupname"]) for g in groups]
    return deform.widget.Select2Widget(values=choices, multiple=True)


def user_select_widget(request):
    users = request.get_collection("morpfw.pas.user").all()
    choices = [(u.userid, u["username"]) for u in users]
    return deform.widget.Select2Widget(values=choices, multiple=True)


@dataclass
class PermissionAssignmentSchema(morpfw.Schema):

    model: typing.Optional[str] = field(
        default=None,
        metadata={"title": "Model", "deform.widget_factory": model_select_widget,},
    )

    permission: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Permission",
            "deform.widget_factory": permission_select_widget,
        },
    )

    groups: typing.Optional[list] = field(
        default_factory=list, metadata={"deform.widget_factory": group_select_widget}
    )
    users: typing.Optional[list] = field(
        default_factory=list, metadata={"deform.widget_factory": user_select_widget}
    )

    rule: typing.Optional[str] = field(
        default="allow",
        metadata={
            "deform.widget": deform.widget.SelectWidget(
                choices=[("allow", "Allow"), ("reject", "Reject")]
            )
        },
    )

    enabled: typing.Optional[bool] = True

    __unique_constraint__ = ["model", "permission", "rule"]
