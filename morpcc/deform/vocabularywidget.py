from colander import Invalid, null
from deform.compat import string_types
from deform.widget import SelectWidget, Widget


class VocabularyWidget(SelectWidget):
    template = "vocabulary"
    readonly_template = "readonly/vocabulary"
    null_value = ""
    values = ()
    multiple = False

    def __init__(self, vocabulary, **kwargs):
        self.vocabulary = vocabulary
        super().__init__(**kwargs)

    def search_url(self, context, request):
        baselink = request.relative_url(
            "/+vocabulary-search?vocabulary={}".format(self.vocabulary)
        )
        return baselink

    def get_label(self, request, identifier):
        vocab = request.app.get_vocabulary(request=request, name=self.vocabulary)
        if vocab is None:
            return ""
        for v in vocab:
            if v["value"] == identifier:
                return v["label"]
        return ""
