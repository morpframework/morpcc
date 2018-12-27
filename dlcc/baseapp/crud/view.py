import re
import rulez
import json
import html
import morepath
from .model import CollectionUI, ModelUI
from ..app import App
from boolean.boolean import ParseError
from ..permission import ViewHome
from ..util import jsonobject_to_colander
import colander
import deform
from morpfw.crud import permission as crudperms


@App.view(model=CollectionUI)
def collection_index(context, request):
    return morepath.redirect(request.link(context, '+%s' % context.default_view))


@App.html(model=CollectionUI, name='listing', template='master/crud/listing.pt',
          permission=crudperms.Search)
def listing(context, request):
    column_options = []
    columns = []
    for c in context.columns:
        columns.append(c['title'])
        sortable = True
        if c['name'].startswith('structure:'):
            sortable = False
        column_options.append({
            'name': c['name'],
            'orderable': sortable
        })
    return {
        'page_title': context.page_title,
        'listing_title': context.listing_title,
        'columns': columns,
        'column_options': json.dumps(column_options)
    }


column_pattern = re.compile(r'^columns\[(\d+)\]\[(\w+)\]$')
search_column_pattern = re.compile(r'^columns\[(\d+)\]\[(\w+)\]\[(\w+)\]$')
search_pattern = re.compile(r'^search\[(\w+)\]$')
order_pattern = re.compile(r'order\[(\d+)\]\[(\w+)\]')


def _parse_dtdata(data):
    result = {}

    result['columns'] = []
    result['search'] = {}
    result['order'] = {}

    columns = [(k, v) for k, v in data if k.startswith('columns')]
    orders = [(k, v) for k, v in data if k.startswith('order')]

    column_data = {}
    for k, v in columns:
        m1 = column_pattern.match(k)
        m2 = search_column_pattern.match(k)
        if m1:
            i, o = m1.groups()
            column_data.setdefault(int(i), {})
            column_data[int(i)][o] = v
        elif m2:
            i, o, s = m2.groups()
            column_data.setdefault(int(i), {})
            column_data[int(i)].setdefault(o, {})
            column_data[int(i)][o][s] = v

    result['columns'] = []
    for k in sorted(column_data.keys()):
        result['columns'].append(column_data[k])

    order_data = {}
    for k, v in orders:
        i, o = order_pattern.match(k).groups()
        order_data.setdefault(int(i), {})
        if o == 'column':
            order_data[int(i)][o] = int(v)
        else:
            order_data[int(i)][o] = v

    result['order'] = []
    for k in sorted(order_data.keys()):
        result['order'].append(order_data[k])

    for k, v in data:
        if k == 'draw':
            result['draw'] = int(v)
        elif k == '_':
            result['_'] = v
        elif k == 'start':
            result['start'] = int(v)
        elif k == 'length':
            result['length'] = int(v)
        elif k.startswith('search'):
            i = search_pattern.match(k).groups()[0]
            result['search'].setdefault(i, {})
            result['search'][i] = v
    return result


@App.json(model=CollectionUI, name='datatable.json', permission=crudperms.View)
def datatable(context, request):
    collection = context.collection
    data = list(request.GET.items())
    data = _parse_dtdata(data)
    search = None
    if data['search']['value']:
        try:
            search = rulez.parse_dsl(data['search']['value'])
        except ValueError:
            pass
        except NotImplementedError:
            pass
        except ParseError:
            pass

    order_by = None
    if data['order']:
        colidx = data['order'][0]['column']
        order_col = data['columns'][colidx]['name']
        if order_col.startswith('structure:'):
            order_by = None
        else:
            order_by = (order_col, data['order'][0]['dir'])
    try:
        objs = collection.search(
            query=search, limit=data['length'], offset=data['start'], order_by=order_by)
    except NotImplementedError:
        objs = collection.search(
            limit=data['length'], offset=data['start'], order_by=order_by)
    total = collection.aggregate(
        group={'count': {'function': 'count', 'field': 'uuid'}})
    rows = []
    for o in objs:
        row = []
        jsonobj = o.data.as_json()
        for c in data['columns']:
            if c['name'].startswith('structure:'):
                row.append(context.get_structure_column(o, request, c['name']))
            else:
                row.append(html.escape(jsonobj[c['name']]))
        rows.append(row)
    return {
        'draw': data['draw'],
        'recordsTotal': total[0]['count'],
        'recordsFiltered': len(rows),
        'data': rows
    }


@App.view(model=ModelUI)
def model_index(context, request):
    return morepath.redirect(request.link(context, '+%s' % context.default_view))


@App.html(model=ModelUI, name='view', template='master/simple-form.pt', permission=crudperms.View)
def view(context, request):
    formschema = jsonobject_to_colander(
        context.model.schema,
        include_fields=context.view_include_fields,
        exclude_fields=context.view_exclude_fields)
    data = context.model.data.as_dict()
    return {
        'page_title': 'View %s' % html.escape(str(context.model.__class__.__name__)),
        'form_title': 'View',
        'form': deform.Form(formschema(), buttons=('Submit',)),
        'form_data': data,
        'readonly': True
    }


@App.html(model=ModelUI, name='edit', template='master/simple-form.pt',
          permission=crudperms.Edit)
def edit(context, request):
    formschema = jsonobject_to_colander(
        context.model.schema, include_fields=context.edit_include_fields,
        exclude_fields=context.edit_exclude_fields)
    data = context.model.data.as_dict()
    return {
        'page_title': 'Edit %s' % html.escape(str(context.model.__class__.__name__)),
        'form_title': 'Edit',
        'form': deform.Form(formschema(), buttons=('Submit',)),
        'form_data': data,
    }


@App.html(model=ModelUI, name='delete', template='master/crud/delete.pt',
          permission=crudperms.Delete)
def delete(context, request):

    formschema = jsonobject_to_colander(
        context.model.schema,
        include_fields=context.view_include_fields,
        exclude_fields=context.view_exclude_fields)
    data = context.model.data.as_dict()
    return {
        'page_title': 'Delete Confirmation',
        'form_title': 'Are you sure you want to delete this?',
        'form': deform.Form(formschema()),
        'form_data': data
    }


@App.html(model=CollectionUI, name='create', template='master/simple-form.pt',
          permission=crudperms.Create)
def create(context, request):
    formschema = jsonobject_to_colander(
        context.collection.schema, include_fields=context.create_include_fields,
        exclude_fields=context.create_exclude_fields)
    return {
        'page_title': 'Create %s' % html.escape(
            str(context.collection.__class__.__name__.replace('Collection', ''))),
        'form_title': 'Create',
        'form': deform.Form(formschema(), buttons=('Submit',)),
    }
