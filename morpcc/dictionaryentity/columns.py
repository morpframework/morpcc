from ..app import App
from .model import DictionaryEntityModel


@App.structure_column(model=DictionaryEntityModel, name="buttons")
def get_buttons_column(model, request, name):
    results = ""
    uiobj = model.ui()

    buttons = [
        {
            "icon": "eye",
            "data-url": request.relative_url(
                "/dictionaryelement/+datatable.json?filter=dictionaryentity_uuid%3D%3D{}".format(
                    model.uuid
                )
            ),
            "data-create-url": request.relative_url(
                "/dictionaryelement/+modal-create?dictionaryentity_uuid={}".format(
                    model.uuid
                )
            ),
            "title": "View",
            "class": "dictionaryentity-view-link",
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
