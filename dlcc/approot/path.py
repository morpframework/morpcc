from ..app import App
from .model import AppRoot, StaticRoot


@App.path(model=AppRoot, path='/')
def get_approot():
    return AppRoot()


@App.path(model=StaticRoot, path='/static', absorb=True)
def get_staticroot(absorb):
    return StaticRoot(absorb)
