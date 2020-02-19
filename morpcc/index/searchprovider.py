import rulez
from morpfw.crud.searchprovider.base import SearchProvider

from ..app import App
from ..datamodel.path import get_collection as get_dm_collection
from .model import IndexContentCollection


class IndexSearchProvider(SearchProvider):
    def parse_query(self, qs):
        if qs is None:
            return None
        if not qs.strip():
            return None
        return {"field": "searchabletext", "operator": "match", "value": qs}

    def search(self, query=None, offset=0, limit=None, order_by=None):
        idxcol = self.context
        lorder_by = []
        order_by = order_by or []
        indexes = [idx["name"] for idx in idxcol.__parent__.search()]
        for ob in order_by:
            if ob[0] in indexes:
                lorder_by.append(ob)
        if not lorder_by:
            lorder_by = None
        searchres = idxcol.search(query, offset, limit, order_by=lorder_by)
        result = []
        dmcol = get_dm_collection(self.context.request)
        cached_dm = {}
        for sr in searchres:
            dm = cached_dm.get(sr["datamodel_uuid"], None)
            if dm is None:
                dm = dmcol.get(sr["datamodel_uuid"])
                cached_dm[sr["datamodel_uuid"]] = dm

            if dm is None:
                continue

            ccol = dm.content_collection()
            item = ccol.get(sr["datamodel_content_uuid"])
            result.append(item)

        return result


@App.searchprovider(model=IndexContentCollection)
def get_searchprovider(context):
    return IndexSearchProvider(context)
