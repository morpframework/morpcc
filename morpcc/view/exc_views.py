import morpfw
import morepath
from morepath.authentication import NO_IDENTITY
from webob.exc import HTTPNotFound, HTTPForbidden, HTTPInternalServerError
import urllib.parse
from ..app import App
from ..root import Root


@App.view(model=HTTPNotFound)
def httpnotfound_error(context, request: morepath.Request):

    @request.after
    def adjust_status(response):
        response.status = 404

    if request.path.startswith('/api/'):
        return morepath.render_json({
            'status': 'error',
            'message': 'Object Not Found : %s' % request.path}, request)
    else:
        render = request.app.config.template_engine_registry.get_template_render(
            'master/error_404.pt', morepath.render_html)
        return render({}, request)


@App.view(model=HTTPForbidden)
def forbidden_error(context, request):
    @request.after
    def nocache(response):
        response.headers.add('Cache-Control', 'no-store')

    print('identity')
    print(request.identity)
    if request.identity is NO_IDENTITY and not request.path.startswith('/api/'):
        return morepath.redirect(
            request.relative_url('/login?came_from=%s' % urllib.parse.quote(request.url)))

    @request.after
    def adjust_status(response):
        response.status = 403
#   FIXME: should log this when a config for DEBUG_SECURITY is enabled
#    logger.error(traceback.format_exc())
    if request.path.startswith('/api/'):
        return morepath.render_json({
            'status': 'error',
            'message': 'Access Denied : %s' % request.path}, request)
    else:
        render = request.app.config.template_engine_registry.get_template_render(
            'master/error_403.pt', morepath.render_html
        )
        return render({}, request)
