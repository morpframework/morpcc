import json
import os
import pprint
import tempfile
import typing

import morpfw.crud.storage.sqlstorage
import rulez
import sqlalchemy
import sqlalchemy_jsonfield.jsonfield
import sqlalchemy_utils
from alembic.autogenerate.api import (
    AutogenContext,
    compare_metadata,
    produce_migrations,
    render,
)
from alembic.autogenerate.compare import comparators
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.operations.ops import UpgradeOps
from morpfw.crud.schemaconverter.dataclass2pgsqla import dataclass_to_pgsqla
from RestrictedPython import compile_restricted, safe_globals
from sqlalchemy import MetaData, create_engine
from sqlalchemy.schema import CreateSchema

from ..app import App
from ..attribute.path import get_collection as get_attr_collection
from ..backrelationship.path import get_collection as get_brel_collection
from ..dictionaryelement.path import get_collection as get_del_collection
from ..dictionaryentity.path import get_collection as get_dent_collection
from ..entity.path import get_collection as get_dm_collection
from ..referencedata.path import get_collection as get_refdata_collection
from ..referencedatakey.path import get_collection as get_refdatakey_collection
from ..referencedataproperty.path import get_collection as get_refdataprop_collection
from ..relationship.path import get_collection as get_rel_collection
from .model import ApplicationModel
from .path import get_collection as get_app_collection


def render_python_code(
    up_or_down_op,
    sqlalchemy_module_prefix="sa.",
    alembic_module_prefix="op.",
    render_as_batch=False,
    imports=(),
    render_item=None,
):
    """Render Python code given an :class:`.UpgradeOps` or
    :class:`.DowngradeOps` object.

    This is a convenience function that can be used to test the
    autogenerate output of a user-defined :class:`.MigrationScript` structure.

    """
    opts = {
        "sqlalchemy_module_prefix": sqlalchemy_module_prefix,
        "alembic_module_prefix": alembic_module_prefix,
        "user_module_prefix": None,
        "render_item": render_item,
        "render_as_batch": render_as_batch,
    }

    autogen_context = AutogenContext(None, opts=opts)
    autogen_context.imports = set(imports)
    return render._indent(render._render_cmd_body(up_or_down_op, autogen_context))


def _get_migrate_function(code):
    byte_code = compile_restricted(code, filename="<inline code>", mode="exec")
    glob = safe_globals.copy()
    glob.update(
        {
            "sa": sqlalchemy,
            "sqlalchemy_jsonfield": sqlalchemy_jsonfield,
            "morpfw": morpfw,
            "sqlalchemy_utils": sqlalchemy_utils,
        }
    )
    loc = {}
    exec(byte_code, glob, loc)
    return loc["migrate"]


class ApplicationDatabaseSyncAdapter(object):
    def __init__(self, context: ApplicationModel, request):
        self.context = context
        self.request = request
        self.session = self.request.get_db_session("warehouse")
        self.engine = create_engine(self.session.bind.url)

        self.content_metadata = context.content_metadata()

        with self.engine.connect() as conn:
            # conn.dialect.default_schema_name = self.content_metadata.schema
            migration_context = MigrationContext.configure(
                conn, opts={"include_schemas": False}
            )
            self.upgrade_steps = self.get_upgrade_steps(migration_context)
            if len(self.upgrade_steps.ops):
                self.need_update = True
            else:
                self.need_update = False
            self.migration_code = self.get_migration_code()

    def get_upgrade_steps(self, migration_context) -> typing.List:
        content_metadata = self.context.content_metadata()
        content_metadata.clear()
        dmcol = get_dm_collection(self.request)
        for dm in dmcol.search(rulez.field["application_uuid"] == self.context["uuid"]):
            dc = dm.dataclass()
            tbl = dataclass_to_pgsqla(dc, content_metadata)
        upgrade_ops = UpgradeOps([])
        autogen_context = AutogenContext(migration_context, content_metadata)
        schemas = [content_metadata.schema]
        comparators.dispatch("schema", autogen_context.dialect.name)(
            autogen_context, upgrade_ops, schemas
        )
        return upgrade_ops

    def get_migration_code(self):
        ops = self.upgrade_steps
        mcode = render_python_code(ops)
        code = ""
        for l in mcode.split("\n"):
            if not l.strip().startswith("#"):
                code += l + "\n"
        code = "def migrate(op):\n{}".format(code)

        return code

    def update(self):
        code = self.migration_code
        migrate = _get_migrate_function(code)
        schema_name = self.context.content_metadata().schema

        with self.engine.connect() as conn:
            migration_context = MigrationContext.configure(
                conn, opts={"include_schemas": False}
            )
            op = Operations(migration_context)
            if not self.engine.dialect.has_schema(self.engine, schema_name):
                conn.execute(CreateSchema(schema_name))
            migrate(op)

    def list_update_actions(self) -> typing.List[dict]:
        return self.upgrade_steps.as_diffs()

    def close(self):
        migration_context = MigrationContext.configure(
            conn, opts={"include_schemas": False}
        )
        self.conn.close()


class AttributesBrowser(object):
    def __init__(self, entity, request):
        self.entity = entity
        self.col = get_attr_collection(request)

    def __getitem__(self, key):
        attrs = self.col.search(
            rulez.and_(
                rulez.field["entity_uuid"] == self.entity.uuid,
                rulez.field["name"] == key,
            )
        )
        if attrs:
            return attrs[0]
        return None

    def keys(self):
        return [
            i["name"]
            for i in self.col.search(rulez.field["entity_uuid"] == self.entity.uuid)
        ]


class RelationshipsBrowser(AttributesBrowser):
    def __init__(self, entity, request):
        self.entity = entity
        self.col = get_rel_collection(request)


class BackRelationshipsBrowser(AttributesBrowser):
    def __init__(self, entity, request):
        self.entity = entity
        self.col = get_brel_collection(request)


class EntityNavigator(object):
    def __init__(self, entity, request):
        self.entity = entity
        self.request = request
        self.content_collection = entity.content_collection()
        self.attr_col = get_attr_collection(request)
        self.rel_col = get_rel_collection(request)
        self.brel_col = get_brel_collection(request)
        self.attributes = AttributesBrowser(entity, request)
        self.relationships = RelationshipsBrowser(entity, request)
        self.backrelationships = RelationshipsBrowser(entity, request)

    def search(self, *args, **kwargs):
        return self.content_collection.search(*args, **kwargs)

    def create(self, data, deserialize=False):
        return self.content_collection.create(data, deserialize=deserialize)

    def add_attribute(
        self,
        name,
        type_,
        title,
        description=None,
        required=False,
        primary_key=False,
        dictionaryelement=None,
        allow_invalid=False,
    ):
        data = {
            "name": name,
            "type": type_,
            "title": title,
            "description": description,
            "required": required,
            "primary_key": primary_key,
            "entity_uuid": self.entity.uuid,
            "dictionaryelement_uuid": None,
            "allow_invalid": allow_invalid,
        }
        if dictionaryelement:
            data["dictionaryelement_uuid"] = dictionaryelement.uuid

        return self.attr_col.create(data, deserialize=False)

    def add_relationship(
        self,
        name,
        title,
        reference_attribute,
        reference_search_attribute,
        description=None,
        required=False,
        primary_key=False,
    ):
        data = {
            "name": name,
            "title": title,
            "description": description,
            "reference_attribute_uuid": reference_attribute.uuid,
            "reference_search_attribute_uuid": reference_search_attribute.uuid,
            "required": required,
            "primary_key": primary_key,
            "entity_uuid": self.entity.uuid,
        }

        return self.rel_col.create(data, deserialize=False)

    def add_backrelationship(
        self,
        name,
        title,
        reference_relationship,
        description=None,
        single_relation=False,
    ):

        data = {
            "name": name,
            "title": title,
            "description": description,
            "entity_uuid": self.entity.uuid,
            "reference_relationship_uuid": reference_relationship.uuid,
            "single_relation": single_relation,
        }

        return self.brel_col.create(data, deserialize=False)


class ApplicationNavigator(object):
    def __init__(self, application, request):
        self.application = application
        self.request = request
        self.entity_col = get_dm_collection(request)
        self.entities = {}
        for entity in self.entity_col.search(
            rulez.field["application_uuid"] == self.application.uuid,
        ):
            self.entities[entity["name"]] = entity

    def __getitem__(self, key):
        return self.entities[key]

    def keys(self):
        return self.entities.keys()

    def values(self) -> typing.List[EntityNavigator]:
        return [EntityNavigator(e, self.request) for e in self.entities.values()]

    def add_entity(
        self, name, title, icon="database"
    ) -> typing.Optional[EntityNavigator]:
        data = {
            "name": name,
            "title": title,
            "icon": icon,
            "application_uuid": self.application.uuid,
        }
        entity = self.entity_col.create(data, deserialize=False)
        if entity:
            return EntityNavigator(entity, self.request)
        return None


class RefDataKeyNavigator(object):
    def __init__(self, refdatakey, request):
        self.refdatakey = refdatakey
        self.request = request
        self.prop_col = get_refdataprop_collection(request)

    def add_property(self, name, value):
        data = {
            "name": name,
            "value": value,
            "referencedatakey_uuid": self.refdatakey.uuid,
        }
        prop = self.prop_col.create(data, deserialize=False)
        return prop

    def __getitem__(self, key):
        props = self.prop_col.search(
            rulez.and_(
                rulez.field["referencedatakey_uuid"] == self.refdatakey.uuid,
                rulez.field["name"] == key,
            )
        )
        if props:
            return props[0]
        return KeyError(key)

    def keys(self):
        return [
            p["name"]
            for p in self.prop_col.search(
                rulez.field["referencedatakey_uuid"] == self.refdatakey.uuid
            )
        ]


class RefDataNavigator(object):
    def __init__(self, refdata, request):
        self.refdata = refdata
        self.request = request
        self.key_col = get_refdatakey_collection(request)

    def add_key(self, name, description=None) -> typing.Optional[RefDataKeyNavigator]:
        data = {
            "name": name,
            "referencedata_uuid": self.refdata.uuid,
            "description": description,
        }
        key = self.key_col.create(data, deserialize=False)
        if key:
            return RefDataKeyNavigator(key, self.request)
        return None

    def __getitem__(self, key) -> RefDataKeyNavigator:
        keys = self.key_col.search(
            rulez.and_(
                rulez.field["referencedata_uuid"] == self.refdata.uuid,
                rulez.field["name"] == key,
            )
        )
        if keys:
            return RefDataKeyNavigator(keys[0], self.request)
        raise KeyError(key)

    def keys(self):
        return [
            k["name"]
            for k in self.key_col.search(
                rulez.field["referencedata_uuid"] == self.refdata.uuid
            )
        ]


class DictionaryEntityNavigator(object):
    def __init__(self, dictentity, request):
        self.dictentity = dictentity
        self.request = request
        self.element_col = get_del_collection(request)

    def add_element(
        self,
        name,
        title,
        type_,
        referencedata_name=None,
        referencedata_property="label",
    ):
        data = {
            "name": name,
            "title": title,
            "type": type_,
            "dictionaryentity_uuid": self.dictentity.uuid,
            "referencedata_name": referencedata_name,
            "referencedata_property": referencedata_property,
        }
        el = self.element_col.create(data, deserialize=False)
        return el

    def __getitem__(self, key):
        elements = self.element_col.search(
            rulez.and_(
                rulez.field["dictionaryentity_uuid"] == self.dictentity.uuid,
                rulez.field["name"] == key,
            )
        )
        if elements:
            return elements[0]
        raise KeyError(key)

    def keys(self):
        return [
            e["name"]
            for e in self.element_col.search(
                rulez.field["dictionaryentity_uuid"] == self.dictentity.uuid
            )
        ]


class DataDictionaryBrowser(object):
    def __init__(self, request):
        self.request = request
        self.dictentity_col = get_dent_collection(request)

    def __getitem__(self, key):
        dents = self.dictentity_col.search(rulez.field["name"] == key)
        if dents:
            return DictionaryEntityNavigator(dents[0], self.request)
        raise KeyError(key)

    def keys(self):
        return [e["name"] for e in self.dictentity_col.search()]


class Navigator(object):
    def __init__(self, request):
        self.request = request
        self.app_col = get_app_collection(request)
        self.refdata_col = get_refdata_collection(request)
        self.dictentity_col = get_dent_collection(request)
        self.datadictionary = DataDictionaryBrowser(request)
        self.apps = {}
        for app in self.app_col.search():
            self.apps[app["name"]] = app

    def __getitem__(self, key) -> ApplicationNavigator:
        if key not in apps.keys():
            raise KeyError(key)
        return ApplicationNavigator(self.apps[key], self.request)

    def keys(self):
        return self.apps.keys()

    def values(self):
        return [ApplicationNavigator(a, self.request) for a in self.apps.values()]

    def add_application(
        self, name, title, icon="cube"
    ) -> typing.Optional[ApplicationNavigator]:
        data = {"name": name, "title": title, "icon": icon}
        app = self.app_col.create(data, deserialize=False)
        if app:
            self.apps[app["name"]] = app
            return ApplicationNavigator(app, self.request)
        return None

    def add_referencedata(self, name, title) -> typing.Optional[RefDataNavigator]:
        data = {"name": name, "title": title}
        refdata = self.refdata_col.create(data, deserialize=False)
        if refdata:
            return RefDataNavigator(refdata, self.request)
        return None

    def add_dictionaryentity(
        self, name, title
    ) -> typing.Optional[DictionaryEntityNavigator]:
        data = {"name": name, "title": title}
        dent = self.dictentity_col.create(data, deserialize=False)
        if dent:
            return DictionaryEntityNavigator(dent, self.request)
        return None
