from ..app import App
from ..root import Root
from .. import permission as perm


@App.html(model=Root, name='site-settings', template='master/site-settings.pt',
          permission=perm.ManageSite)
def site_settings(context, request):
    return {
        'setting_modules': [{
            'title': 'Settings',
            'icon': 'wrench',
            'href': request.relative_url('/site-settings/setting/+listing'),
        }, {
            'title': 'Manage Users',
            'icon': 'user',
            'href': request.relative_url('/manage-users/+listing'),
        }, {
            'title': 'Manage Groups',
            'icon': 'group',
            'href': request.relative_url('/manage-groups/+listing'),
        }, {
            'title': 'Manage API Keys',
            'icon': 'key',
            'href': request.relative_url('/manage-apikeys/+listing')
        }, {
            'title': 'Manage Reference Data',
            'icon': 'book',
            'href': request.relative_url('/referencedata/+listing')
        }, {
            'title': 'Manage Applications',
            'icon': 'cubes',
            'href': request.relative_url('/application/+listing')
        }, {
            'title': 'Manage Indexes',
            'icon': 'search',
            'href': request.relative_url('/index/+listing')
        }]
    }
