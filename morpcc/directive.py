import dectate
import morepath
import reg
from morepath.directive import SettingAction

from .permission import ManageSite
from .registry.applicationbehavior import ApplicationBehaviorRegistry
from .registry.behavior import BehaviorRegistry
from .registry.default_factory import DefaultFactoryRegistry
from .registry.portlet import PortletProviderRegistry, PortletRegistry
from .registry.settingpage import SettingPageRegistry

PORTLET_FACTORY_IDS: dict = {}


class PortletFactoryAction(dectate.Action):

    config = {"portlet_registry": PortletRegistry}

    depends = [SettingAction]

    def __init__(self, name, template=None, permission=None):
        self.template = template
        self.name = name
        self.permission = permission

    def identifier(self, portlet_registry: PortletRegistry):
        return self.name

    def perform(self, obj, portlet_registry: PortletRegistry):
        portlet_registry.register(
            obj, name=self.name, template=self.template, permission=self.permission
        )


class PortletProviderFactoryAction(dectate.Action):

    config = {"portletprovider_registry": PortletProviderRegistry}

    depends = [SettingAction]

    def __init__(self, name, permission=None):
        self.name = name
        self.permission = permission

    def identifier(self, portletprovider_registry: PortletProviderRegistry):
        return self.name

    def perform(self, obj, portletprovider_registry: PortletProviderRegistry):
        portletprovider_registry.register(
            obj, name=self.name, permission=self.permission
        )


class StructureColumnAction(dectate.Action):

    app_class_arg = True

    def __init__(self, model, name):
        self.model = model
        self.name = name

    def identifier(self, app_class):
        return str((app_class, self.model, self.name))

    def perform(self, obj, app_class):
        app_class.get_structure_column.register(
            reg.methodify(obj),
            model=self.model,
            request=morepath.Request,
            name=self.name,
        )


class SchemaExtenderAction(dectate.Action):

    app_class_arg = True

    def __init__(self, schema):
        self.schema = schema

    def identifier(self, app_class):
        return str((app_class, self.schema))

    def perform(self, obj, app_class):
        app_class.get_schemaextender.register(reg.methodify(obj), schema=self.schema)


class MessagingProviderAction(dectate.Action):

    app_class_arg = True

    def __init__(self, name):
        self.name = name

    def identifier(self, app_class):
        return str((app_class, self.name))

    def perform(self, obj, app_class):
        app_class.get_messagingprovider.register(
            reg.methodify(obj), request=morepath.Request, name=self.name
        )


class VocabularyAction(dectate.Action):

    app_class_arg = True

    def __init__(self, name):
        self.name = name

    def identifier(self, app_class):
        return str((app_class, self.name))

    def perform(self, obj, app_class):
        app_class.get_vocabulary.register(
            reg.methodify(obj), request=morepath.Request, name=self.name
        )


class IndexerAction(dectate.Action):

    app_class_arg = True

    def __init__(self, model, name):
        self.model = model
        self.name = name

    def identifier(self, app_class):
        return str((app_class, self.model, self.name))

    def perform(self, obj, app_class):
        app_class.get_indexer.register(
            reg.methodify(obj), model=self.model, name=self.name,
        )


class BehaviorAction(dectate.Action):

    config = {"behavior_registry": BehaviorRegistry}

    app_class_arg = True

    depends = [SettingAction]

    def __init__(self, name):
        self.name = name

    def identifier(self, app_class, behavior_registry: BehaviorRegistry):
        return self.name

    def perform(self, obj, app_class, behavior_registry: BehaviorRegistry):
        def factory(name):
            return obj

        app_class.get_behavior_factory.register(reg.methodify(factory), name=self.name)
        behavior_registry.register_behavior(name=self.name)


class ApplicationBehaviorAction(dectate.Action):

    config = {"application_behavior_registry": ApplicationBehaviorRegistry}

    app_class_arg = True

    depends = [SettingAction]

    def __init__(self, name):
        self.name = name

    def identifier(
        self, app_class, application_behavior_registry: ApplicationBehaviorRegistry
    ):
        return self.name

    def perform(
        self, obj, app_class, application_behavior_registry: ApplicationBehaviorRegistry
    ):
        def factory(name):
            return obj

        app_class.get_application_behavior_factory.register(
            reg.methodify(factory), name=self.name
        )
        application_behavior_registry.register_behavior(name=self.name)


class DefaultFactoryAction(dectate.Action):

    config = {"default_factory_registry": DefaultFactoryRegistry}

    app_class_arg = True

    depends = [SettingAction]

    def __init__(self, name):
        self.name = name

    def identifier(self, app_class, default_factory_registry: DefaultFactoryRegistry):
        return self.name

    def perform(self, obj, app_class, default_factory_registry: DefaultFactoryRegistry):
        def factory(name):
            return obj

        app_class.get_default_factory.register(reg.methodify(factory), name=self.name)
        default_factory_registry.register(name=self.name)


class IndexResolverAction(dectate.Action):

    app_class_arg = True

    def __init__(self, name):
        self.name = name

    def identifier(self, app_class):
        return str((app_class, self.name))

    def perform(self, obj, app_class):
        def factory(name):
            return obj

        app_class.get_index_resolver.register(reg.methodify(factory), name=self.name)


class RestrictedModuleAction(dectate.Action):

    app_class_arg = True

    def __init__(self, name):
        self.name = name

    def identifier(self, app_class):
        return str((app_class, self.name))

    def perform(self, obj, app_class):
        app_class.get_restricted_module.register(reg.methodify(obj), name=self.name)


class BreadcrumbAction(dectate.Action):

    app_class_arg = True

    def __init__(self, model):
        self.model = model

    def identifier(self, app_class):
        return str((app_class, self.model))

    def perform(self, obj, app_class):
        app_class.get_breadcrumb.register(
            reg.methodify(obj), model=self.model, request=morepath.Request,
        )


class SettingPageAction(dectate.Action):

    config = {"setting_page_registry": SettingPageRegistry}
    app_class_arg = True

    depends = [SettingAction]

    def __init__(self, name, permission=None, title=None, order=0):
        self.name = name
        if title is None:
            title = name.replace("-", " ").title()
        self.title = title
        self.permission = permission
        self.order = order

    def identifier(self, app_class, setting_page_registry: SettingPageRegistry):
        return str((app_class, self.name))

    def perform(self, obj, app_class, setting_page_registry: SettingPageRegistry):
        setting_page_registry.register(
            obj,
            name=self.name,
            title=self.title,
            permission=self.permission,
            order=self.order,
        )

