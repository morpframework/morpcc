from morepath.toposort import toposorted, Info
from .util import permits


class PortletRegistry(object):

    def __init__(self):
        self._portlet_infos = {}
        self._portlet_options = {}

    def register_portlet_factory(self, portlet_factory, provider, template, over, under):
        self._portlet_infos.setdefault(provider, [])
        self._portlet_infos[provider].append(
            Info(portlet_factory, over, under))
        self._portlet_options.setdefault(provider, {})
        self._portlet_options[provider][portlet_factory] = {
            'factory': portlet_factory,
            'provider': provider,
            'template': template
        }

    def get_provider(self, provider):
        infos = self._portlet_infos[provider]
        portlets = [self._portlet_options[provider][info.key]
                    for info in toposorted(infos)]
        return PortletProvider(provider, portlets)


class PortletProvider(object):

    def __init__(self, name, sorted_portlet_factories):
        self.name = name
        self.sorted_portlet_factories = sorted_portlet_factories

    def render(self, context, request, load_template):
        result = []

        def _permits(permission, request=request, context=context):
            return permits(request, context, permission)

        for portlet in self.sorted_portlet_factories:
            res = portlet['factory'](context, request)
            if portlet['template'] is None:
                assert isinstance(res, str)
                result.append(res)
            else:
                template = load_template(portlet['template'])
                data = {
                    'permits': permits,
                    'app': request.app,
                    'settings': request.app.settings,
                    'request': request,
                    'context': context,
                    'load_template': load_template
                }
                data.update(res)
                result.append(template.render(**data))

        return '\n'.join(result)
