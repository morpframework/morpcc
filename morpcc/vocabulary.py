import json
import os

from .app import App


@App.vocabulary("morpcc.behaviors")
def behaviors(request, name):
    registry = request.app.config.behavior_registry
    return [{"value": n, "label": n} for n in registry.behaviors]


@App.vocabulary("morpcc.application_behaviors")
def application_behaviors(request, name):
    registry = request.app.config.application_behavior_registry
    return [{"value": n, "label": n} for n in registry.behaviors]


CACHED = {}


@App.vocabulary("morpcc.fa-icons")
def fa_icons(request, name):
    icons = CACHED.get("icons", None)

    if icons is None:
        icons_fpath = os.path.join(
            os.path.dirname(__file__), "resources", "fa-icons.json"
        )
        with open(icons_fpath) as icons_file:
            icons = json.loads(icons_file.read())
        CACHED["icons"] = icons

    return [{"value": k, "label": k} for k, v in icons.items()]
