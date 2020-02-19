import html

import deform
import morepath
from deform.widget import HiddenWidget
from morpfw.crud import permission as crudperms
from morpfw.crud.errors import AlreadyExistsError, ValidationError
from webob.exc import HTTPFound

from ...app import App
from ...util import dataclass_to_colander
from ..model import CollectionUI, ModelUI


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
        request=request,
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
        request=request,
        include_fields=context.create_include_fields,
        exclude_fields=context.create_exclude_fields,
    )

    controls = list(request.POST.items())
    form = deform.Form(formschema(), buttons=("Submit",))

    failed = False
    data = {}

    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True
    if not failed:
        try:
            obj = context.collection.create(data, deserialize=False)
        except AlreadyExistsError as e:
            failed = True
            request.notify("error", "Already Exists", "Object already exists")
        except ValidationError as e:
            failed = True
            for form_error in e.form_errors:
                request.notify("error", "Form Validation Error", form_error.message)
            for field_error in e.field_errors:
                request.notify("error", 
                    "Field {} Validation Error".format(field_error.path),
                    field_error.message)

        if not failed:
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
        "form_data": data,
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
