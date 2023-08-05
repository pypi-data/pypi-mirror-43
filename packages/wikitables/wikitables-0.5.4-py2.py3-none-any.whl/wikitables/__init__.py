import json
import logging
import mwparserfromhell as mwp

from wikitables.client import Client
from wikitables.readers import RowReader
from wikitables.util import TableJSONEncoder, ftag, ustr

log = logging.getLogger('wikitables')

def import_tables(article, lang="en"):
    client = Client(lang)
    page = client.fetch_page(article)
    body = page['revisions'][0]['*']

    ## parse for tables
    raw_tables = mwp.parse(body).filter_tags(matches=ftag('table'))

    def _table_gen():
        for idx, table in enumerate(raw_tables):
            name = '%s[%s]' % (page['title'],idx)
            yield WikiTable(name, table)

    return list(_table_gen())

class WikiTable(object):
    """
    Parsed Wikipedia table
    attributes:
     - name(str): Table name in the format <article_name>[<table_index>]
     - head(list): List of parsed column names as strings
     - rows(list): List of <wikitables.Row> objects
    """
    def __init__(self, name, raw_table):
        self.name = ustr(name)
        self.rows = []
        self._head = []
        self._node = raw_table
        self._tr_nodes = raw_table.contents.filter_tags(matches=ftag('tr'))
        self._read_header()
        self._read_rows()

    def json(self):
        return json.dumps(self.rows, cls=TableJSONEncoder)

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, val):
        if not isinstance(val, list):
            raise ValueError('table head must be provided as list')
        self._head = val
        self._read_rows()

    def __repr__(self):
        return "<WikiTable '%s'>" % self.name

    def _log(self, s):
        log.debug('%s: %s' % (self.name, s))

    def _read_rows(self):
        reader = RowReader(self.name, self._head)
        self.rows = list(reader.parse(*self._tr_nodes))
        self._log('parsed %d rows %d cols' % (len(self.rows), len(self._head)))

    def _read_header(self):
        # read header
        header_nodes = self._find_header_flat()
        if not header_nodes:
            header_nodes = self._find_header_row()

        for th in header_nodes:
            field_name = th.contents.strip_code().strip(' ')
            self._head.append(ustr(field_name))

    def _find_header_flat(self):
        """
        Find header elements in a table, if possible. This case handles
        situations where '<th>' elements are not within a row('<tr>')
        """
        nodes = self._node.contents.filter_tags(
                    matches=ftag('th'), recursive=False)
        if not nodes:
            return
        self._log('found header outside rows (%d <th> elements)' % len(nodes))
        return nodes

    def _find_header_row(self):
        """
        Evaluate all rows and determine header position, based on
        greatest number of 'th' tagged elements
        """
        th_max = 0
        header_idx = 0
        for idx, tr in enumerate(self._tr_nodes):
            th_count = len(tr.contents.filter_tags(matches=ftag('th')))
            if th_count > th_max:
                th_max = th_count
                header_idx = idx

        self._log('found header at row %d (%d <th> elements)' % \
                    (header_idx, th_max))

        header_row = self._tr_nodes.pop(header_idx)
        return header_row.contents.filter_tags(matches=ftag('th'))
