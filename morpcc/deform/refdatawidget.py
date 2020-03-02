import rulez
from colander import Invalid, null
from deform.compat import string_types
from deform.widget import SelectWidget, Widget

from ..referencedata.path import get_collection as get_refdata_collection
from ..referencedatakey.path import get_collection as get_refdatakey_collection
from ..referencedataproperty.path import get_collection as get_refdataprop_collection


class ReferenceDataWidget(SelectWidget):
    template = "referencedata"
    readonly_template = "readonly/referencedata"
    null_value = ""
    values = ()
    multiple = False

    def __init__(self, referencedata_name, referencedata_property="label", **kwargs):
        self.referencedata_name = referencedata_name
        self.referencedata_property = referencedata_property
        super().__init__(**kwargs)

    def search_url(self, context, request):
        baselink = request.relative_url(
            "/referencedata/+vocabulary-search?name={}&property={}".format(
                self.referencedata_name, self.referencedata_property
            )
        )
        return baselink

    def get_label(self, request, identifier):
        col = get_refdata_collection(request)
        refdatas = col.search(rulez.field["name"] == self.referencedata_name)
        if not refdatas:
            return ""
        refdata = refdatas[0]

        keycol = get_refdatakey_collection(request)
        keys = keycol.search(
            rulez.and_(
                rulez.field["referencedata_uuid"] == refdata.uuid,
                rulez.field["name"] == identifier,
            )
        )

        if not keys:
            return identifier

        key = keys[0]

        propcol = get_refdataprop_collection(request)
        props = propcol.search(
            rulez.and_(
                rulez.field["referencedatakey_uuid"] == key.uuid,
                rulez.field["name"] == self.referencedata_property,
            )
        )

        if not props:
            return ""

        return props[0]["value"]
