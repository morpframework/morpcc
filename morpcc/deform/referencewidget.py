from deform.widget import Widget, SelectWidget
from deform.compat import string_types
from colander import null
from colander import Invalid


class ReferenceWidget(SelectWidget):
    template = 'reference'
    readonly_template = 'readonly/reference'
    null_value = ""
    values = ()
    multiple = False

    def __init__(self, resource_type, term_field, value_field, **kwargs):
        self.resource_type = resource_type
        self.term_field = term_field
        self.value_field = value_field
        super().__init__(**kwargs)

    def deserialize(self, *args, **kwargs):
        result = super().deserialize(*args, **kwargs)
        print(result)
        return result

    def get_resource_search_url(self, context, request):
        return request.link(context, '+term-search?resource_type=%s&term_field=%s&value_field=%s' % (
            self.resource_type, self.term_field, self.value_field))

    def get_resource_url(self, request, identifier):
        m = self.get_resource(request, identifier)
        return request.link(m)

    def get_resource(self, request, identifier):
        typeinfo = request.app.config.type_registry.get_typeinfo(
            name=self.resource_type, request=request)
        m = typeinfo['model_ui_factory'](request, identifier)
        return m

    def get_resource_term(self, request, identifier):
        m = self.get_resource(request, identifier)
        return m.model[self.term_field]
