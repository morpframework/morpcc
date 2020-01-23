import morepath
import html
import deform
from morpfw.crud import permission as crudperms
from ..model import CollectionUI, ModelUI
from ...app import App
from ...util import dataclass_to_colander
from webob.exc import HTTPFound
from deform.widget import HiddenWidget


@App.html(
    model=CollectionUI,
    name="create",
    template="master/simple-form.pt",
    permission=crudperms.Create,
)
def create(context, request):
    default_value_fields = list(request.GET.keys())
    formschema = dataclass_to_colander(
        context.collection.schema,
        include_fields=context.create_include_fields,
        exclude_fields=context.create_exclude_fields,
        hidden_fields=default_value_fields,
    )

    form_data = {}
    for f in default_value_fields:
        form_data[f] = request.GET.get(f)

    return {
        "page_title": "Create %s"
        % html.escape(
            str(context.collection.__class__.__name__.replace("Collection", ""))
        ),
        "form_title": "Create",
        "form": deform.Form(formschema(), buttons=("Submit",)),
        "form_data": form_data,
    }


@App.html(
    model=CollectionUI,
    name="modal-create",
    template="master/crud/modal-form.pt",
    permission=crudperms.Create,
)
def modal_create(context, request):
    return create(context, request)


@App.html(
    model=CollectionUI,
    name="create",
    template="master/simple-form.pt",
    permission=crudperms.Create,
    request_method="POST",
)
def process_create(context, request):
    formschema = dataclass_to_colander(
        context.collection.schema,
        include_fields=context.create_include_fields,
        exclude_fields=context.create_exclude_fields,
    )

    controls = list(request.POST.items())
    form = deform.Form(formschema(), buttons=("Submit",))

    failed = False
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True

    if not failed:
        obj = context.collection.create(data)
        return morepath.redirect(
            request.link(context.modelui_class(request, obj, context))
        )

    return {
        "page_title": "Create %s"
        % html.escape(
            str(context.collection.__class__.__name__.replace("Collection", ""))
        ),
        "form_title": "Create",
        "form": form,
    }


@App.html(
    model=CollectionUI,
    name="modal-create",
    template="master/crud/modal-form.pt",
    permission=crudperms.Create,
    request_method="POST",
)
def modal_process_create(context, request):
    result = process_create(context, request)

    if isinstance(result, HTTPFound):
        return morepath.redirect(request.link(context, "+modal-close"))
    return result
