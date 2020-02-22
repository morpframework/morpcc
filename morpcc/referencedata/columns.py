from ..app import App
from .model import ReferenceEntity


@App.structure_column(model=ReferenceEntity, name="buttons")
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
                "/referencedatakey/+datatable.json?filter=referencedata_uuid%3D%3D{}".format(
                    model.uuid
                )
            ),
            "data-create-url": request.relative_url(
                "/referencedatakey/+modal-create?referencedata_uuid={}".format(
                    model.uuid
                )
            ),
            "title": "View",
            "class": "refdata-view-link",
        },
        {
            "icon": "download",
            "url": request.link(uiobj, "+export"),
            "title": "Download",
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
        results += '<a title="%(title)s" ' % button
        if button.get("class", None):
            results += 'class="%(class)s" ' % button
        if button.get("data-url", None):
            results += 'data-url="%(data-url)s" ' % button
        if button.get("data-create-url", None):
            results += 'data-create-url="%(data-create-url)s" ' % button
        if button.get("url", None):
            results += 'href="%(url)s"> ' % button
        else:
            results += 'href="#"> '
        results += '<i class="fa fa-%(icon)s"></i></a> ' % button
    return results
