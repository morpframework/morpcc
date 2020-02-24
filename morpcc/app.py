import functools
import os
from uuid import uuid4

import dectate
import morepath
import morpfw
import reg
from beaker.middleware import SessionMiddleware as BeakerMiddleware
from more.chameleon import ChameleonApp
from morepath.publish import resolve_model
from morpfw.app import DBSessionRequest
from morpfw.authn.pas.policy import SQLStorageAuthApp, SQLStorageAuthnPolicy
from morpfw.authz.pas import DefaultAuthzPolicy
from morpfw.main import create_app
from webob.exc import HTTPException

from . import directive
from .authn import IdentityPolicy


class WebAppRequest(DBSessionRequest):
    def notify(self, category, title, message):
        session = self.environ["beaker.session"]
        session.setdefault("messages", [])
        session["messages"].append(
            {"category": category, "title": title, "message": message}
        )
        session.save()

    def messages(self):
        session = self.environ["beaker.session"]
        result = session.get("messages", [])
        session["messages"] = []
        session.save()
        return result

    @property
    def session(self):
        return self.environ["beaker.session"]


class App(ChameleonApp, morpfw.SQLApp, DefaultAuthzPolicy):

    request_class = WebAppRequest

    portlet = dectate.directive(directive.PortletFactoryAction)
    portletprovider = dectate.directive(directive.PortletProviderFactoryAction)
    structure_column = dectate.directive(directive.StructureColumnAction)
    schemaextender = dectate.directive(directive.SchemaExtenderAction)
    messagingprovider = dectate.directive(directive.MessagingProviderAction)
    vocabulary = dectate.directive(directive.VocabularyAction)
    indexer = dectate.directive(directive.IndexerAction)
    indexresolver = dectate.directive(directive.IndexResolverAction)
    behavior = dectate.directive(directive.BehaviorAction)
    application_behavior = dectate.directive(directive.ApplicationBehaviorAction)

    @reg.dispatch_method(reg.match_instance("model"), reg.match_key("name"))
    def get_indexer(self, model, name):
        return None

    @reg.dispatch_method(
        reg.match_instance("model"),
        reg.match_instance("request"),
        reg.match_key("name"),
    )
    def get_structure_column(self, model, request, name):
        raise NotImplementedError(
            "Get structure columns for %s structure:%s" % (model, name)
        )

    def get_portletprovider(self, name):
        return self.config.portletprovider_registry.get_provider(name)

    @reg.dispatch_method(reg.match_class("schema"))
    def get_schemaextender(self, schema):
        return schema

    @reg.dispatch_method(reg.match_instance("request"), reg.match_key("name"))
    def get_messagingprovider(self, request, name):
        raise NotImplementedError("Messaging provider %s is not available" % name)

    @reg.dispatch_method(reg.match_instance("request"), reg.match_key("name"))
    def get_vocabulary(self, request, name):
        return None

    @reg.dispatch_method(reg.match_key("name"))
    def get_behavior_factory(self, name):
        raise NotImplementedError

    @reg.dispatch_method(reg.match_key("name"))
    def get_application_behavior_factory(self, name):
        raise NotImplementedError

    @reg.dispatch_method(reg.match_key("name"))
    def get_index_resolver(self, name):
        raise NotImplementedError

    def render_view(self, context, request, name=""):
        lookup = self.get_view.by_predicates(model=context.__class__, name=name)
        if lookup and lookup.component:
            try:
                return lookup.component(obj=context, request=request, app=self)
            except HTTPException as e:
                return None
        return None


class AuthnPolicy(SQLStorageAuthnPolicy):
    def get_identity_policy(self, settings):
        config = settings.configuration.__dict__
        if config.get("app.development_mode", True):
            secure = False
        else:
            secure = True

        master_secret = config.get("morpfw.security.jwt", {}).get(
            "master_secret", uuid4().hex
        )

        jwt_settings = config.get("morpfw.security.jwt").copy()
        if not "master_secret" in jwt_settings:
            jwt_settings["master_secret"] = master_secret

        itsdangerous_settings = {"secure": secure, "secret": master_secret}

        return IdentityPolicy(
            jwt_settings=jwt_settings,
            itsdangerous_settings=itsdangerous_settings,
            api_root="/api",
            development_mode=config.get("app.development_mode", True),
        )


App.hook_auth_models(prefix="/api/v1/auth")


def create_morpcc_app(settings, scan=True, **kwargs):
    application = create_app(settings=settings, scan=scan, **kwargs)
    if (
        settings["beaker_session"].get("session.type", None) is None
        and settings["beaker_session"].get("session.url", None) is None
    ):
        settings["beaker_session"]["session.type"] = settings["configuration"].get(
            "morpcc.beaker.session.type"
        )
        settings["beaker_session"]["session.url"] = settings["configuration"].get(
            "morpcc.beaker.session.url"
        )

    return BeakerMiddleware(application, settings["beaker_session"])
