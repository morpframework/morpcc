import morepath
import html
import deform
from morpfw.crud import permission as crudperms
from ..model import CollectionUI, ModelUI
from ...app import App
from ...util import dataclass_to_colander
from webob.exc import HTTPNotFound, HTTPFound


@App.html(
    model=ModelUI,
    name="edit",
    template="master/crud/form.pt",
    permission=crudperms.Edit,
)
def edit(context, request):
    formschema = dataclass_to_colander(
        context.model.schema,
        include_fields=context.edit_include_fields,
        exclude_fields=context.edit_exclude_fields,
    )
    data = context.model.data.as_dict()
    return {
        "page_title": "Edit %s" % html.escape(str(context.model.__class__.__name__)),
        "form_title": "Edit",
        "form": deform.Form(formschema(), buttons=("Submit",)),
        "form_data": data,
    }


@App.html(
    model=ModelUI,
    name="modal-edit",
    template="master/crud/modal-form.pt",
    permission=crudperms.Edit,
)
def modal_edit(context, request):
    return edit(context, request)


@App.html(
    model=ModelUI,
    name="edit",
    template="master/crud/form.pt",
    permission=crudperms.Edit,
    request_method="POST",
)
def process_edit(context, request):
    formschema = dataclass_to_colander(
        context.model.schema,
        include_fields=context.edit_include_fields,
        exclude_fields=context.edit_exclude_fields,
    )
    data = context.model.data.as_dict()
    controls = list(request.POST.items())
    form = deform.Form(formschema(), buttons=("Submit",))

    failed = False
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True
    if not failed:
        # FIXME: model update should allow datetime object
        prov = request.app.get_dataprovider(
            context.model.schema, data, context.model.storage
        )
        context.model.update(prov.as_json())
        return morepath.redirect(request.link(context))

    return {
        "page_title": "Edit %s" % html.escape(str(context.model.__class__.__name__)),
        "form_title": "Edit",
        "form": form,
        "form_data": data,
    }


@App.html(
    model=ModelUI,
    name="modal-edit",
    template="master/crud/modal-form.pt",
    permission=crudperms.Edit,
    request_method="POST",
)
def modal_process_edit(context, request):
    result = process_edit(context, request)
    if isinstance(result, HTTPFound):
        return morepath.redirect(request.link(context, "+modal-close"))
    return result


@App.html(
    model=ModelUI,
    name="xattredit",
    template="master/crud/form.pt",
    permission=crudperms.Edit,
)
def xattredit(context, request):

    xattrprovider = context.model.xattrprovider()
    if xattrprovider:
        xattrformschema = dataclass_to_colander(xattrprovider.schema)
    else:
        raise HTTPNotFound()

    data = xattrprovider.as_dict()
    return {
        "page_title": "Edit %s Extended Attributes"
        % html.escape(str(context.model.__class__.__name__)),
        "form_title": "Edit Extended Attributes",
        "form": deform.Form(xattrformschema(), buttons=("Submit",)),
        "form_data": data,
    }


@App.html(
    model=ModelUI,
    name="modal-xattredit",
    template="master/crud/modal-form.pt",
    permission=crudperms.Edit,
)
def modal_xattredit(context, request):
    return xattredit(context, request)


@App.html(
    model=ModelUI,
    name="xattredit",
    template="master/crud/form.pt",
    permission=crudperms.Edit,
    request_method="POST",
)
def process_xattredit(context, request):

    xattrprovider = context.model.xattrprovider()
    if xattrprovider:
        xattrformschema = dataclass_to_colander(xattrprovider.schema)
    else:
        raise HTTPNotFound()

    data = xattrprovider.as_dict()
    controls = list(request.POST.items())
    form = deform.Form(xattrformschema(), buttons=("Submit",))

    failed = False
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True
    if not failed:
        # FIXME: model update should allow datetime object
        xattrprovider.update(data)
        return morepath.redirect(request.link(context))

    return {
        "page_title": "Edit %s" % html.escape(str(context.model.__class__.__name__)),
        "form_title": "Edit",
        "form": form,
        "form_data": data,
    }


@App.html(
    model=ModelUI,
    name="modal-xattredit",
    template="master/crud/modal-form.pt",
    permission=crudperms.Edit,
    request_method="POST",
)
def modal_process_xattredit(context, request):
    result = process_xattredit(context, request)
    if isinstance(result, HTTPFound):
        return morepath.redirect(request.link(context, "+modal-close"))
    return result

