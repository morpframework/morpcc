import morepath
from morpfw.authn.pas.policy import JWTWithAPIKeyIdentityPolicy
from more.itsdangerous import IdentityPolicy as ItsDangerousIdentityPolicy


class IdentityPolicy(morepath.IdentityPolicy):

    def __init__(self, jwt_settings, itsdangerous_settings, api_root='/api'):
        self.api_root = api_root
        self.jwtpolicy = JWTWithAPIKeyIdentityPolicy(**jwt_settings)
        self.itsdangerouspolicy = ItsDangerousIdentityPolicy(
            **itsdangerous_settings)

    def getpolicy(self, request):
        if request.cookies.get('userid'):
            return self.itsdangerouspolicy
        if request.path.startswith(self.api_root):
            return self.jwtpolicy
        return self.itsdangerouspolicy

    def identify(self, request: morepath.Request):
        policy = self.getpolicy(request)
        return policy.identify(request)

    def remember(self, response, request, identity):
        policy = self.getpolicy(request)
        return policy.remember(response, request, identity)

    def forget(self, response, request):
        policy = self.getpolicy(request)
        return policy.forget(response, request)
