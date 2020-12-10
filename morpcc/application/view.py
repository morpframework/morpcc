import morpfw
import rulez
from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from ..app import App
from ..entity.path import get_collection as get_dm_collection
from ..entitycontent.model import content_collection_factory
from ..index.path import get_collection as get_index_collection
from .adapters import ApplicationDatabaseSyncAdapter
from .model import ApplicationModel
from .modelui import ApplicationModelUI


@App.html(
    model=ApplicationModelUI,
    name="view",
    template="master/application/view.pt",
    permission=crudperm.View,
)
def view(context, request):
    result = default_view(context, request)
    dmcol = get_dm_collection(request)
    dbsync = ApplicationDatabaseSyncAdapter(context.model, request)
    if dbsync.need_update:
        if context["state"] == "active":
            return morpfw.redirect(request.link(context, "+schema-upgrade"))
        result["pending_upgrade"] = True
        return result
    entities = dmcol.search(rulez.field["schema_uuid"] == context.model["schema_uuid"])
    entities = [
        content_collection_factory(entity, context.model) for entity in entities
    ]
    result["entities"] = sorted(entities, key=lambda x: x.__parent__["title"])
    result["pending_upgrade"] = False
    return result


@App.html(
    model=ApplicationModelUI,
    name="edit",
    template="master/application/edit.pt",
    permission=crudperm.Edit,
)
def edit(context, request):
    result = default_edit(context, request)
    result["page_title"] = "Edit: %s" % (context.model["title"])
    return result


@App.html(
    model=ApplicationModelUI,
    name="schema-upgrade",
    template="master/application/schema-upgrade.pt",
    permission=crudperm.Edit,
)
def schema_upgrade(context, request):
    dbsync = ApplicationDatabaseSyncAdapter(context.model, request)
    if not dbsync.need_update:
        return morpfw.redirect(request.link(context))
    code = dbsync.migration_code
    formatter = HtmlFormatter()
    highlighted = highlight(code, PythonLexer(), formatter)
    return {
        "hide_title": True,
        "need_update": dbsync.need_update,
        "code": code,
        "highlighted_code": highlighted,
        "highlight_styles": formatter.get_style_defs(".highlight"),
    }


@App.view(
    model=ApplicationModelUI,
    name="schema-upgrade",
    permission=crudperm.Edit,
    request_method="POST",
)
def process_schema_upgrade(context, request):
    run = request.POST.get("action", "").lower()
    if run != "update":
        request.notify("error", "Error", "Invalid operation")
        return morpfw.redirect(request.link(context))
    sm = context.model.statemachine()
    sm.upgrade()
    request.notify("success", "Processing .. ", "Database update triggered")
    return morpfw.redirect(request.link(context))


@App.json(model=ApplicationModelUI, name="search.json", permission=crudperm.View)
def search(context, request):
    col = get_index_collection(request).content_collection()
    prov = col.searchprovider()
    qs = prov.parse_query(request.GET.get("q", None))
    res = []
    search = rulez.field["application_uuid"] == context.model.uuid
    if qs:
        search = rulez.and_(search, qs)
    for obj in prov.search(search):
        res.append(obj.json())
    return res
