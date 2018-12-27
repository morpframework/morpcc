import jsonobject
import colander


def jsonobject_property_to_colander_schemanode(
        prop: jsonobject.JsonProperty, oid_prefix='deformField') -> colander.SchemaNode:
    if isinstance(prop, jsonobject.DateProperty):
        return colander.SchemaNode(typ=colander.Date(),
                                   name=prop.name,
                                   oid='%s-%s' % (oid_prefix, prop.name),
                                   missing=colander.required if prop.required else colander.drop)
    if isinstance(prop, jsonobject.DateTimeProperty):
        return colander.SchemaNode(typ=colander.DateTime(),
                                   name=prop.name,
                                   oid='%s-%s' % (oid_prefix, prop.name),
                                   missing=colander.required if prop.required else colander.drop)
    if isinstance(prop, jsonobject.StringProperty):
        return colander.SchemaNode(typ=colander.String(),
                                   name=prop.name,
                                   oid='%s-%s' % (oid_prefix, prop.name),
                                   missing=colander.required if prop.required else colander.drop)
    if isinstance(prop, jsonobject.IntegerProperty):
        return colander.SchemaNode(typ=colander.Integer(),
                                   name=prop.name,
                                   oid='%s-%s' % (oid_prefix, prop.name),
                                   missing=colander.required if prop.required else colander.drop)
    if isinstance(prop, jsonobject.FloatProperty):
        return colander.SchemaNode(typ=colander.Float(),
                                   name=prop.name,
                                   oid='%s-%s' % (oid_prefix, prop.name),
                                   missing=colander.required if prop.required else colander.drop)
    if isinstance(prop, jsonobject.BooleanProperty):
        return colander.SchemaNode(typ=colander.Boolean(),
                                   name=prop.name,
                                   oid='%s-%s' % (oid_prefix, prop.name),
                                   missing=colander.required if prop.required else colander.drop)

    if isinstance(prop, jsonobject.DictProperty):
        if prop.item_wrapper:
            subtype = jsonobject_to_colander(
                prop.item_wrapper.item_type, colander_schema_type=colander.MappingSchema)

            return subtype()
        return colander.SchemaNode(typ=colander.Mapping(),
                                   name=prop.name,
                                   oid='%s-%s' % (oid_prefix, prop.name),
                                   missing=colander.required if prop.required else colander.drop)
    if isinstance(prop, jsonobject.ListProperty):
        if prop.item_wrapper:
            if isinstance(prop.item_wrapper, jsonobject.ObjectProperty):
                if issubclass(prop.item_wrapper.item_type, jsonobject.JsonObject):
                    subtype = jsonobject_to_colander(
                        prop.item_wrapper.item_type, colander_schema_type=colander.MappingSchema)
                    return subtype()
        return colander.SchemaNode(
            typ=colander.List(),
            name=prop.name,
            oid='%s-%s' % (oid_prefix, prop.name),
            missing=colander.required if prop.required else colander.drop)

    raise KeyError(prop)


def jsonobject_to_colander(schema,
                           include_fields=None,
                           exclude_fields=None,
                           colander_schema_type=colander.MappingSchema):
    # output colander schema from jsonobject schema
    attrs = {}

    include_fields = include_fields or []
    exclude_fields = exclude_fields or []

    if include_fields:
        for attr, prop in schema._properties_by_attr.items():
            if prop.name in include_fields and prop.name not in exclude_fields:
                prop = jsonobject_property_to_colander_schemanode(
                    prop)
                attrs[attr] = prop
    else:
        for attr, prop in schema._properties_by_attr.items():
            if prop.name not in exclude_fields:
                prop = jsonobject_property_to_colander_schemanode(
                    prop)
                attrs[attr] = prop

    Schema = type("Schema", (colander_schema_type, ), attrs)

    return Schema
