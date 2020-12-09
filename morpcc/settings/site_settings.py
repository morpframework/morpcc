from morpfw.crud import permission as crudperm

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
    modules = []
    if request.permits("/site-settings/setting", crudperm.Search):
        modules.append(
            {
                "title": "Settings",
                "icon": "wrench",
                "href": request.relative_url("/site-settings/setting/+listing"),
            }
        )
    if request.permits("/manage-users", crudperm.Search):
        modules.append(
            {
                "title": "Manage Users",
                "icon": "user",
                "href": request.relative_url("/manage-users/+listing"),
            },
        )
    if request.permits("/manage-groups", crudperm.Search):
        modules.append(
            {
                "title": "Manage Groups",
                "icon": "group",
                "href": request.relative_url("/manage-groups/+listing"),
            }
        )

    if request.permits("/manage-apikeys", crudperm.Search):
        modules.append(
            {
                "title": "Manage API Keys",
                "icon": "key",
                "href": request.relative_url("/manage-apikeys/+listing"),
            }
        )

    if request.permits("/permissionassignment", crudperm.Search):
        modules.append(
            {
                "title": "Manage Permissions",
                "icon": "shield",
                "href": request.relative_url("/permissionassignment/+listing"),
            }
        )

    if request.permits("/schema", crudperm.Search):
        modules.append(
            {
                "title": "Manage Schemas",
                "icon": "file-code-o",
                "href": request.relative_url("/schema/+listing"),
            }
        )

    if request.permits("/referencedata", crudperm.Search):
        modules.append(
            {
                "title": "Manage Reference Data",
                "icon": "book",
                "href": request.relative_url("/referencedata/+listing"),
            }
        )

    if request.permits("/attributevalidator", crudperm.Search):
        modules.append(
            {
                "title": "Manage Attribute Validators",
                "icon": "check-circle",
                "href": request.relative_url("/attributevalidator/+listing"),
            },
        )

    if request.permits("/entityvalidator", crudperm.Search):
        modules.append(
            {
                "title": "Manage Entity Validators",
                "icon": "check-square",
                "href": request.relative_url("/entityvalidator/+listing"),
            }
        )

    if request.permits("/dictionaryentity", crudperm.Search):
        modules.append(
            {
                "title": "Manage Data Dictionary",
                "icon": "book",
                "href": request.relative_url("/dictionaryentity/+listing"),
            }
        )

    if request.permits("/application", crudperm.Search):
        modules.append(
            {
                "title": "Manage Applications",
                "icon": "cubes",
                "href": request.relative_url("/application/+listing"),
            }
        )

    if request.permits("/endpoint", crudperm.Search):
        modules.append(
            {
                "title": "Manage API Endpoints",
                "icon": "code",
                "href": request.relative_url("/endpoint/+listing"),
            }
        )

    if request.permits("/index", crudperm.Search):
        modules.append(
            {
                "title": "Manage Indexes",
                "icon": "search",
                "href": request.relative_url("/index/+listing"),
            }
        )

    if request.permits("/process", crudperm.Search):
        modules.append(
            {
                "title": "Background Processes",
                "icon": "gears",
                "href": request.relative_url("/process/+listing"),
            }
        )
    if request.permits("/activitylog", crudperm.Search):
        modules.append(
            {
                "title": "Activity / Audit Log",
                "icon": "history",
                "href": request.relative_url("/activitylog"),
            }
        )
    return {"page_title": "Site Settings", "setting_modules": modules}
