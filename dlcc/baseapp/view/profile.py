import morepath
import colander
import deform
import deform.widget
from morpfw.auth.user.path import get_user
from ..app import App, SQLAuthApp
from ..root import Root
from .. import permission


class PersonalInfoSchema(colander.MappingSchema):
    username = colander.SchemaNode(
        colander.String(),
        missing='',
        widget=deform.widget.TextInputWidget(template='readonly/textinput'))
    email = colander.SchemaNode(
        colander.String(), validator=colander.Email(msg="Invalid e-mail address"))
    state = colander.SchemaNode(
        colander.String(),
        missing='',
        widget=deform.widget.TextInputWidget(template='readonly/textinput'))
    created = colander.SchemaNode(
        colander.DateTime(),
        widget=deform.widget.DateTimeInputWidget(template='readonly/datetimeinput'))
    password_current = colander.SchemaNode(colander.String(),
                                           title="Current password",
                                           widget=deform.widget.PasswordWidget(),
                                           missing='')

    password = colander.SchemaNode(colander.String(),
                                   title="New password",
                                   widget=deform.widget.PasswordWidget(),
                                   missing='')
    password_confirm = colander.SchemaNode(colander.String(),
                                           widget=deform.widget.PasswordWidget(),
                                           title="Confirm new password",
                                           missing='')


def personalinfo_form() -> deform.Form:
    return deform.Form(PersonalInfoSchema(), buttons=('Submit',))


@App.html(model=Root, name='profile', template="master/simple-form.pt",
          permission=permission.EditOwnProfile)
def profile(context, request: morepath.Request):
    form = personalinfo_form()
    userid = request.identity.userid
    newreq = request.copy(app=request.app.get_authnz_provider())
    user = get_user(newreq, userid)
    return {
        'page_title': 'Profile',
        'form_title': 'Personal Information',
        'form': form,
        'readonly': False,
        'form_data': user.data.as_dict()
    }


@App.html(model=Root, name='profile', request_method='POST',
          template='master/simple-form.pt', permission=permission.EditOwnProfile)
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
