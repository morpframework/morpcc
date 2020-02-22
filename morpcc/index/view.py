import morpfw
from morpcc import permission as mccperm
from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from ..app import App
from ..root import Root
from .adapter import IndexDatabaseSyncAdapter
from .model import IndexCollectionUI
from .path import get_collection


@App.html(
    model=IndexCollectionUI,
    name="schema-upgrade",
    template="master/application/schema-upgrade.pt",
    permission=crudperm.Edit,
)
def schema_upgrade(context, request):
    dbsync = IndexDatabaseSyncAdapter(context.collection, request)
    if not dbsync.need_update:
        return morpfw.redirect(request.link(context))
    code = dbsync.migration_code
    formatter = HtmlFormatter()
    highlighted = highlight(code, PythonLexer(), formatter)
    return {
        "need_update": dbsync.need_update,
        "code": code,
        "highlighted_code": highlighted,
        "highlight_styles": formatter.get_style_defs(".highlight"),
    }


@App.view(
    model=IndexCollectionUI,
    name="schema-upgrade",
    permission=crudperm.Edit,
    request_method="POST",
)
def process_schema_upgrade(context, request):
    run = request.POST.get("action", "").lower()
    if run != "update":
        request.notify("error", "Error", "Invalid operation")
        return morpfw.redirect(request.link(context))
    dbsync = IndexDatabaseSyncAdapter(context.collection, request)
    if dbsync.need_update:
        dbsync.update()
    request.notify("success", "Success", "Database updated")
    return morpfw.redirect(request.link(context))


def _search(context, request):
    col = get_collection(request).content_collection()
    prov = col.searchprovider()
    search = prov.parse_query(request.GET.get("q", None))
    res = []
    if search is None:
        return {"results": []}
    for entry in prov.search(search):
        obj = entry.get_object()
        if obj is None:
            continue
        r = {
            "title": entry["title"],
            "description": entry["description"],
            "preview": entry["preview"],
            "url": request.link(obj.ui()),
        }
        res.append(r)
    return {"results": res}


@App.json(
    model=Root, name="search.json", permission=mccperm.SiteSearch,
)
def search_json(context, request):
    return _search(context, request)


@App.html(
    model=Root,
    name="site-search",
    template="master/site-search.pt",
    permission=mccperm.SiteSearch,
)
def search(context, request):
    return _search(context, request)


@App.html(
    model=IndexCollectionUI,
    name="listing",
    permission=crudperm.View,
    template="master/index/listing.pt",
)
def listing(context, request):
    result = default_listing(context, request)
    dbsync = IndexDatabaseSyncAdapter(context.collection, request)
    result["need_update"] = dbsync.need_update
    return result
