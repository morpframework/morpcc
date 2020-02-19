from ..app import App
from .model import ReferenceDataKeyModel


@App.structure_column(model=ReferenceDataKeyModel, name="buttons")
def get_buttons_column(model, request, name):
    results = ""
    typeinfos = request.app.config.type_registry.get_typeinfos(request)
    uiobj = None
    # FIXME: have a nicer API through typeregistry
    for n, ti in typeinfos.items():
        if model.__class__ == ti["model"]:
            uiobj = ti["model_ui"](request, model, ti["collection_ui_factory"](request))
            break
    if uiobj is None:
        raise ValueError("Unable to locate typeinfo for %s" % model)

    buttons = [
        {
            "icon": "eye",
            "data-url": request.relative_url(
                "/referencedataproperty/+datatable.json?filter=referencedatakey_uuid%3D%3D{}".format(
                    model.uuid
                )
            ),
            "data-create-url": request.relative_url(
                "/referencedataproperty/+modal-create?referencedatakey_uuid={}".format(
                    model.uuid
                )
            ),
            "title": "View",
            "class": "refdatakey-view-link",
        },
        {
            "icon": "edit",
            "data-url": request.link(uiobj, "+modal-edit"),
            "title": "Edit",
            "class": "modal-link",
        },
        {
            "icon": "trash",
            "data-url": request.link(uiobj, "+modal-delete"),
            "title": "Delete",
            "class": "modal-link",
        },
    ]
    for button in buttons:
        results += '<a title="%(title)s" class="%(class)s" ' % button
        results += 'data-url="%(data-url)s" ' % button
        if button.get("data-create-url", None):
            results += 'data-create-url="%(data-create-url)s" ' % button
        results += 'href="#"> '
        results += '<i class="fa fa-%(icon)s"></i></a> ' % button
    return results
