import morepath
import colander
import deform
from deform.widget import PasswordWidget
from ..app import App
from ..root import Root


class PersonalInfoSchema(colander.MappingSchema):
    email = colander.SchemaNode(
        colander.String(), validator=colander.Email(msg="Invalid e-mail address"))
    password = colander.SchemaNode(colander.String(),
                                   widget=PasswordWidget(),
                                   missing='')
    password_confirm = colander.SchemaNode(colander.String(),
                                           widget=PasswordWidget(),
                                           missing='')


def personalinfo_form() -> deform.Form:
    return deform.Form(PersonalInfoSchema(), buttons=('Submit',))


@App.html(model=Root, name='profile', template="master/simple-form.pt")
def profile(context, request):
    form = personalinfo_form()
    return {
        'page_title': 'Profile',
        'form_title': 'Personal Information',
        'form': form,
        'readonly': True,
        'form_data': {
            'email': 'izhar@abyres.net'
        }
    }


@App.html(model=Root, name='profile', request_method='POST',
          template='master/simple-form.pt')
def process_profile(context, request):
    form = personalinfo_form()
    controls = request.POST.items()
    try:
        appstruct = form.validate(controls)
    except deform.ValidationFailure as e:
        return {
            'form': e,
            'page_title': 'Profile',
            'form_title': 'Personal Information',
        }

    return morepath.redirect(request.url)
