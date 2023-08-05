"""this contains the cube-specific entities' classes"""

from cubicweb.entities import AnyEntity, fetch_config


class Card(AnyEntity):
    """customized class for Card entities"""
    __regid__ = 'Card'
    rest_attr = 'wikiid'

    fetch_attrs, cw_fetch_order = fetch_config(['title'])

    def dc_title(self):
        if self.wikiid:
            return self.wikiid.split('/')[-1]
        else:
            return self.title

    def dc_description(self, format='text/plain'):
        return self.printable_value('synopsis', format=format)

    def rest_path(self):
        if self.wikiid:
            return '%s/%s' % (str(self.e_schema).lower(),
                              self._cw.url_quote(self.wikiid, safe='/'))
        else:
            return super(Card, self).rest_path()
