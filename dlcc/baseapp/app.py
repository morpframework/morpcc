import os
import morpfw
from morpfw.app import DBSessionRequest
from morpfw.auth.app import App as AuthApp
from more.chameleon import ChameleonApp
import morepath
from morepath.publish import resolve_model
import functools


class App(ChameleonApp, morpfw.SQLApp):
    pass
