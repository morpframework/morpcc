import rulez
from morpfw.crud import permission as crudperm

from ...app import App
from ...deform.referencewidget import ReferenceWidget
from ..model import CollectionUI, ModelUI
from .listing import datatable_search


@App.json(model=ModelUI, name="backreference-search.json", permission=crudperm.View)
def reference_content_search(context, request):
    bref_name = request.GET.get("backreference_name", "").strip()
    if not bref_name:
        return {}

    brefs = context.model.backreferences()
    bref = brefs[bref_name]
    collectionui = bref.collection(request).ui()

    ref = bref.get_reference(request)
    return datatable_search(
        collectionui,
        request,
        additional_filters=rulez.field(ref.name) == context.model[ref.attribute],
    )
