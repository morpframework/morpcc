from .app import App


@App.portlet('left-portlets', template='master/portlet/navigation.pt')
def navigation_portlet(context, request):
    types = request.app.config.type_registry.get_typeinfos(request)
    types_nav = []
    for typeinfo in types.values():
        types_nav.append({
            'title': typeinfo['title'],
            'href': request.link(typeinfo['collection_ui_factory'](request))
        })
    types_nav.sort(key=lambda x: x['title'])
    return {
        'navtree': [{
            'section': 'General',
            'children': [
                {'title': 'Home', 'icon': 'home',
                    'children': [
                        {'title': 'Home', 'href': '/'}
                    ]},
                {'title': 'Collections', 'icon': 'database',
                    'children': types_nav}
            ]
        }, {
            'section': 'Administrative',
            'children': [
                {'title': 'Settings',
                 'icon': 'cog',
                 'children': [{
                     'title': 'User',
                     'href': request.relative_url('/manage-users/+listing'),
                 }, {
                     'title': 'Group',
                     'href': request.relative_url('/manage-groups/+listing'),
                 }, {
                     'title': 'API Keys',
                     'href': request.relative_url('/manage-apikeys/+listing')
                 }, {
                     'title': 'Personal',
                     'href': request.relative_url('/personal-settings')
                 }]}
            ]
        }]
    }


@App.portlet('left-portlets', template='master/portlet/profile.pt', over=navigation_portlet)
def profile_portlet(context, request):
    return {}
