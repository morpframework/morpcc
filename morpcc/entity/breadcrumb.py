from ..app import App
from .modelui import EntityModelUI


@App.breadcrumb(model=EntityModelUI)
def get_entity_model_breadcrumb(model, request):
    view_title = None
    if request.view_name:
        view_title = request.view_name.replace("-", " ").title()

    model_crumb = {
        "title": model.model["title"],
        "url": request.link(model),
        "active": False,
    }

    schema_typeinfo = request.app.get_typeinfo("morpcc.schema", request)
    schema = model.model.entity_schema()
    schema_crumb = {
        "title": schema["title"],
        "url": request.link(schema.ui()),
        "active": False,
    }

    schema_collection_crumb = {
        "title": schema_typeinfo["title"],
        "url": request.link(schema.collection.ui()),
        "active": False,
    }
    crumbs = [schema_collection_crumb, schema_crumb, model_crumb]
    if view_title:
        return crumbs + [
            {
                "title": view_title,
                "url": request.link(model, "+" + request.view_name),
                "active": True,
            }
        ]

    model_crumb["active"] = True
    return crumbs
