from ..app import App
from ..root import Root
from .. import permission as perm


@App.html(model=Root, name='site-settings', template='master/site-settings.pt',
          permission=perm.ManageSite)
def site_settings(context, request):
    return {
        'setting_modules': [{
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
        }]
    }
