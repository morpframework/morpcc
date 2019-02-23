import morepath
import colander
import deform
import deform.widget
from morpfw.crud.model import Model
from morpfw.authn.pas.user.path import get_user_collection
from morpfw.crud import permission as crudperm
from ..tempstore import FSBlobFileUploadTempStore
import morpfw.authn.pas.exc
from ...app import App, SQLAuthApp
from ... import permission
from ...util import dataclass_to_colander
from ..model import ModelUI


def upload_form(context: ModelUI, request: morepath.Request) -> deform.Form:
    fields = {}
    model = context.model
    for f in model.blob_fields:
        fields[f] = colander.SchemaNode(
            deform.FileData(),
            missing=colander.drop,
            widget=deform.widget.FileUploadWidget(
                FSBlobFileUploadTempStore(f, context, request, '/tmp/tempstore')),
            oid='file-upload-%s' % f)

    FileUpload = type("FileUpload", (colander.Schema, ), fields)

    return deform.Form(FileUpload(), buttons=('Upload', ), formid='upload-form')


@App.html(model=ModelUI, name='upload', permission=crudperm.Edit,
          template='master/crud/form.pt')
def upload(context, request):
    data = {}
    for f in context.model.blob_fields:
        blob = context.model.get_blob(f)
        if blob is None:
            continue
        data[f] = {
            'uid': blob.uuid,
            'filename': blob.filename,
            'size': blob.size,
            'mimetype': blob.mimetype,
            'download_url': request.link(context.model, '+blobs?field=%s' % f),
            'preview_url': request.link(context, '+blob-preview?field=%s' % f)
        }

    return {
        'page_title': 'Upload',
        'form_title': 'Upload',
        'form': upload_form(context, request),
        'form_data': data
    }


@App.html(model=ModelUI, name='upload', permission=crudperm.Edit,
          template='master/simple-form.pt', request_method='POST')
def process_upload(context, request):
    form = upload_form(context, request)
    controls = list(request.POST.items())

    failed = False
    data = {}
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        failed = True
        form = e

    if not failed:
        for f in context.model.blob_fields:
            if f not in data:
                continue
            filedata = data[f]
            context.model.put_blob(f, filedata['fp'], filename=filedata['filename'],
                                   mimetype=filedata['mimetype'])
        request.notify('success', 'Upload successful',
                       'Files successfully uploaded')
        return morepath.redirect(request.link(context))

    return {
        'page_title': 'Upload',
        'form_title': 'Upload',
        'form': form,
        'form_data': data if not failed else None
    }
