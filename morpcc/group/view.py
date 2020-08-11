import html
import typing
from dataclasses import dataclass, field

import colander
import deform.widget
import morepath
from inverter import dc2colander
from morpfw.crud import permission as crudperms
from morpfw.crud.errors import AlreadyExistsError, ValidationError

from ..app import App
from .model import GroupModelUI


def member_select_widget(request):
    usercol = request.get_collection("morpfw.pas.user")
    choices = []
    for user in usercol.all():
        choices.append((user.userid, user["username"]))
    return deform.widget.Select2Widget(values=choices, multiple=True)


@dataclass
class GroupEditForm(object):

    groupname: typing.Optional[str] = field(default=None, metadata={"editable": False})
    members: typing.List[str] = field(
        default_factory=list, metadata={"deform.widget_factory": member_select_widget},
    )


@App.html(
    model=GroupModelUI,
    name="edit",
    permission=crudperms.Edit,
    template="master/crud/form.pt",
)
def edit(context, request):
    schema = dc2colander.convert(GroupEditForm, request, mode="edit")
    form = deform.Form(schema(), buttons=("Submit",))
    data = {
        "groupname": context.model["groupname"],
        "members": [m.userid for m in context.model.members()],
    }

    return {
        "page_title": "Edit %s" % html.escape(str(context.model.__class__.__name__)),
        "form_title": "Edit",
        "form": form,
        "form_data": data,
    }


@App.html(
    model=GroupModelUI,
    name="edit",
    permission=crudperms.Edit,
    template="master/crud/form.pt",
    request_method="POST",
)
def process_edit(context, request):
    formschema = dc2colander.convert(
        GroupEditForm, request=request, mode="edit-process",
    )
    fs = formschema()
    fs = fs.bind(context=context, request=request)
    controls = list(request.POST.items())
    form = deform.Form(fs, buttons=("Submit",))

    failed = False
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True
    if not failed:
        try:
            context.model.remove_members([m.userid for m in context.model.members()])
            context.model.add_members(data["members"])
        except ValidationError as e:
            failed = True
            for fe in e.field_errors:
                node = form
                if fe.path in form:
                    node = form[fe.path]
                node_error = colander.Invalid(node.widget, fe.message)
                node.widget.handle_error(node, node_error)
        if not failed:
            return morepath.redirect(request.link(context))

    @request.after
    def set_header(response):
        response.headers.add("X-MORP-FORM-FAILED", "True")

    return {
        "page_title": "Edit %s" % html.escape(str(context.model.__class__.__name__)),
        "form_title": "Edit",
        "form": form,
        "form_data": data,
    }
