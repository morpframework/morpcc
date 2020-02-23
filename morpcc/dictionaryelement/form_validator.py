def valid_refdata(context, request, data, mode=None):
    refdataname = (data.get("referencedata_name", None) or "").strip()
    if refdataname:
        if data["type"] != "string":
            return "Reference data can only be assigned to String types"
