from .app import App

@App.vocabulary("morpcc.behaviors")
def behaviors(request, name):
    registry = request.app.config.behavior_registry
    return [{'value': n, 'label': n} for n in registry.behaviors]
