from .. import permission as perm
from ..app import App
from ..root import Root


@App.html(
    model=Root,
    name="site-settings",
    template="master/site-settings.pt",
    permission=perm.ManageSite,
)
def site_settings(context, request):
    return {
        "setting_modules": [
            {
                "title": "Settings",
                "icon": "wrench",
                "href": request.relative_url("/site-settings/setting/+listing"),
            },
            {
                "title": "Manage Users",
                "icon": "user",
                "href": request.relative_url("/manage-users/+listing"),
            },
            {
                "title": "Manage Groups",
                "icon": "group",
                "href": request.relative_url("/manage-groups/+listing"),
            },
            {
                "title": "Manage API Keys",
                "icon": "key",
                "href": request.relative_url("/manage-apikeys/+listing"),
            },
            {
                "title": "Manage Permissions",
                "icon": "shield",
                "href": request.relative_url("/permissionassignment/+listing"),
            },
            {
                "title": "Manage Schemas",
                "icon": "file-code-o",
                "href": request.relative_url("/schema/+listing"),
            },
            {
                "title": "Manage Reference Data",
                "icon": "book",
                "href": request.relative_url("/referencedata/+listing"),
            },
            {
                "title": "Manage Attribute Validators",
                "icon": "check-circle",
                "href": request.relative_url("/attributevalidator/+listing"),
            },
            {
                "title": "Manage Entity Validators",
                "icon": "check-square",
                "href": request.relative_url("/entityvalidator/+listing"),
            },
            {
                "title": "Manage Data Dictionary",
                "icon": "book",
                "href": request.relative_url("/dictionaryentity/+listing"),
            },
            {
                "title": "Manage Applications",
                "icon": "cubes",
                "href": request.relative_url("/application/+listing"),
            },
            {
                "title": "Manage API Endpoints",
                "icon": "code",
                "href": request.relative_url("/endpoint/+listing"),
            },
            {
                "title": "Manage Indexes",
                "icon": "search",
                "href": request.relative_url("/index/+listing"),
            },
            {
                "title": "Background Processes",
                "icon": "gears",
                "href": request.relative_url("/process/+listing"),
            },
        ]
    }
