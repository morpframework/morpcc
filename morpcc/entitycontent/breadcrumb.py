from ..app import App
from .modelui import EntityContentCollectionUI, EntityContentModelUI


@App.breadcrumb(model=EntityContentCollectionUI)
def get_breadcrumb(model, request):
    view_title = None
    if request.view_name:
        view_title = request.view_name.replace("-", " ").title()

    app_typeinfo = request.app.get_typeinfo("morpcc.application", request)

    app = model.collection.application()
    appcol = app.collection
    entity = model.collection.entity()

    crumbs = [
        {
            "title": app_typeinfo["title"],
            "url": request.link(appcol.ui()),
            "active": False,
        },
        {"title": app.title(), "url": request.link(app.ui()), "active": False},
        {"title": entity.title(), "url": request.link(model), "active": False},
    ]

    if view_title:
        return crumbs + [
            {
                "title": view_title,
                "url": request.link(model, "+" + request.view_name),
                "active": True,
            }
        ]

    crumbs[-1]["active"] = True
    return crumbs


@App.breadcrumb(model=EntityContentModelUI)
def get_breadcrumb(model, request):
    view_title = None
    if request.view_name:
        view_title = request.view_name.replace("-", " ").title()

    app_typeinfo = request.app.get_typeinfo("morpcc.application", request)

    app = model.collection_ui.collection.application()
    appcol = app.collection
    entity = model.collection_ui.collection.entity()

    entity_col = app.entity_collections()[entity["name"]]

    crumbs = [
        {
            "title": app_typeinfo["title"],
            "url": request.link(appcol.ui()),
            "active": False,
        },
        {"title": app.title(), "url": request.link(app.ui()), "active": False},
        {
            "title": entity.title(),
            "url": request.link(entity_col.ui()),
            "active": False,
        },
        {"title": model.model.title(), "url": request.link(model), "active": False},
    ]

    if view_title:
        return crumbs + [
            {
                "title": view_title,
                "url": request.link(model, "+" + request.view_name),
                "active": True,
            }
        ]

    crumbs[-1]["active"] = True
    return crumbs
