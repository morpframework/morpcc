def valid_refdata(request, schema, data, mode=None, **kw):
    refdataname = (data.get("referencedata_name", None) or "").strip()
    if refdataname:
        if data["type"] != "string":
            return {
                "field": "type",
                "message": "Reference data can only be assigned to String types",
            }
