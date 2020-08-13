from ..app import App
from .modelui import SchemaModelUI


@App.breadcrumb(model=SchemaModelUI)
def get_breadcrumb(model, request):
    view_title = None
    if request.view_name:
        view_title = request.view_name.replace("-", " ").title()

    schemacol = request.get_collection("morpcc.schema")
    typeinfo = request.app.get_typeinfo("morpcc.schema", request)

    crumbs = [
        {
            "title": typeinfo["title"],
            "url": request.link(schemacol.ui()),
            "active": False,
        },
        {"title": model.model["title"], "url": request.link(model), "active": False},
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
