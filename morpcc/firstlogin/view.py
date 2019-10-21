from ..app import App
from ..root import Root
from ..permission import ViewHome
from ..wizard import FormWizardStep, Wizard, AgreementWizardStep, WizardStep
from ..wizard import ConditionalBlockerWizardStep
from morpfw.authn.pas.user.path import get_user_collection
from dataclasses import dataclass, field
from datetime import datetime
import morepath


class SplashStep(WizardStep):

    title = "Welcome"
    template = 'master/firstlogin-welcome.pt'

    def splash_url(self):
        return 'https://via.placeholder.com/400x150.png'


class EmailVerificationStep(ConditionalBlockerWizardStep):

    title = "Email Verification"
    blocker_error_msg = "You have yet to validate your email address"

    def validate(self):
        return False


@dataclass
class FirstLoginForm(object):

    firstname: str = field(metadata={'required': True})
    lastname: str = field(metadata={'required': True})
    displayname: str = field(metadata={'required': True})


class PersonalInfoStep(FormWizardStep):

    title = 'Personal Information'

    @property
    def schema(self):
        return self.request.app.get_schemaextender(FirstLoginForm)

    def finalize(self):
        data = self.sessiondata
        user = get_user_collection(
            self.request).get_by_userid(self.request.identity.userid)

        xattrprovider = user.xattrprovider()
        xattrprovider.update(data)


class TNCStep(AgreementWizardStep):

    title = 'Terms & Conditions'

    agreement_error_msg = "You must agree to the terms & condition"
    agreement_checkbox_label = "I agree to the terms & condition"

    @property
    def agreement_text(self):
        return "Foobar"

    def finalize(self):
        data = self.sessiondata
        user = get_user_collection(
            self.request).get_by_userid(self.request.identity.userid)

        xattrprovider = user.xattrprovider()
        xattrprovider.update({
            'agreed_terms': True,
            'agreed_terms_ts': int(datetime.utcnow().timestamp())
        })


class FirstLoginWizard(Wizard):

    steps = [SplashStep, EmailVerificationStep, PersonalInfoStep, TNCStep]

    def finalize(self):
        user = get_user_collection(
            self.request).get_by_userid(self.request.identity.userid)

        sm = user.statemachine()
        breakpoint()
        sm.initialize()
        self.clear()
        return morepath.redirect(self.request.relative_url('/'))


@App.html(model=Root, name='firstlogin', permission=ViewHome, template='master/firstlogin.pt')
def firstlogin(context, request):
    return {
        'page_title': 'Welcome!',
        'wizard': FirstLoginWizard(context, request, 'morpcc-firstlogin')
    }


@App.html(model=Root, name='firstlogin', permission=ViewHome,
          template='master/wizard/process.pt',  request_method='POST')
def firstlogin_process(context, request):
    wizard = FirstLoginWizard(context, request, 'morpcc-firstlogin')
    return wizard.handle()
