import dectate
from morepath.directive import SettingAction
from .portletregistry import PortletRegistry
from .typeregistry import TypeRegistry

PORTLET_FACTORY_IDS: dict = {}


class PortletFactoryAction(dectate.Action):

    config = {
        'portlet_registry': PortletRegistry
    }

    depends = [SettingAction]

    filter_convert = {
        'under': dectate.convert_dotted_name,
        'over': dectate.convert_dotted_name
    }

    def __init__(self, provider, template=None, under=None, over=None, name=None):
        PORTLET_FACTORY_IDS.setdefault(provider, 0)
        if name is None:
            name = u'portlet_factory_%s_%s' % (
                provider, PORTLET_FACTORY_IDS[provider])
            PORTLET_FACTORY_IDS[provider] += 1
        self.provider = provider
        self.template = template
        self.under = under
        self.over = over
        self.name = name

    def identifier(self, portlet_registry: PortletRegistry):
        return self.name

    def perform(self, obj, portlet_registry: PortletRegistry):
        portlet_registry.register_portlet_factory(
            obj, provider=self.provider,
            template=self.template,
            over=self.over,
            under=self.under
        )


class TypeInfoFactoryAction(dectate.Action):

    config = {
        'type_registry': TypeRegistry
    }

    depends = [SettingAction]

    def __init__(self, name):
        self.name = name

    def identifier(self, type_registry: TypeRegistry):
        return self.name

    def perform(self, obj, type_registry: TypeRegistry):
        type_registry.register_typeinfo_factory(
            info_factory=obj, name=self.name)
