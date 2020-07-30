from .app import App
from .root import Root

VIEW_TITLES = {"": "Home"}


@App.breadcrumb(model=Root)
def get_root_breadcrumb(model, request):
    view_title = VIEW_TITLES.get(request.view_name, None)
    if not view_title and request.view_name:
        view_title = request.view_name.replace("-", " ").title()
    if view_title:
        return [
            {
                "title": view_title,
                "url": request.link(model, request.view_name),
                "active": True,
            }
        ]
    return []
