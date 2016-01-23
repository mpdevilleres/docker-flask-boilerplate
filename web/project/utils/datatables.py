# -*- coding: utf-8 -*-
import sys

from sqlalchemy.sql.expression import asc, desc
from sqlalchemy.sql import or_, and_
from sqlalchemy.orm.properties import RelationshipProperty
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.expression import cast
from sqlalchemy import String

from collections import namedtuple
from logging import getLogger

log = getLogger(__file__)

if sys.version_info > (3, 0):
    unicode = str

ColumnTuple = namedtuple(
    'ColumnDT',
    ['column_name', 'mData', 'search_like', 'filter', 'searchable'])


def get_attr(sqla_object, attribute):
    """Returns the value of an attribute of an SQLAlchemy entity
    """
    output = sqla_object
    for x in attribute.split('.'):
        if type(output) is InstrumentedList:
            output = ', '.join([getattr(elem, x) for elem in output])
        else:
            output = getattr(output, x)
    return output


class ColumnDT(ColumnTuple):

    """Class defining a DataTables Column with a ColumnTuple:
    :param column_name: name of the column as defined by the SQLAlchemy model
    :type column_name: str
    :param mData: name of the mData property as defined in the
        DataTables javascript options (default None)
    :type mData: str
    :param search_like: is the search made in the middle of the column value.
        If not, the column value must equals to the search value (default True)
    :type search_like: bool
    :param filter: the method needed to be executed on the cell
        values of the column
    as an equivalent of a jinja2 filter (default None)
    :type filter: a callable object
    :param searchable: Enable or disable a column to be searchable
        server-side. (default True)
    :type searchable: bool
    :returns: a ColumnDT object
    """
    def __new__(cls, column_name, mData=None, search_like=True,
                filter=str, searchable=True):
        """
        On creation, sets default None values for mData and string value for
        filter (cause: Object representation is not JSON serializable)
        """
        return super(ColumnDT, cls).__new__(cls, column_name, mData, search_like, filter, searchable)


class DataTables:

    """Class defining a DataTables object with:
    :param request: request containing the GET values, specified by the
        datatable for filtering, sorting and paging
    :type request: pyramid.request
    :param sqla_object: your SQLAlchemy table object
    :type sqla_object: sqlalchemy.ext.declarative.DeclarativeMeta
    :param query: the query wanted to be seen in the the table
    :type query: sqlalchemy.orm.query.Query
    :param columns: columns specification for the datatables
    :type columns: list
    :returns: a DataTables object
    """

    def __init__(self, request, sqla_object, query, columns):
        """Initializes the object with the attributes needed, and runs the query
        """
        self.request_values = DataTables.prepare_arguments(request)
        self.sqla_object = sqla_object
        self.query = query
        self.columns = columns
        self.results = None

        # total in the table after filtering
        self.cardinality_filtered = 0

        # total in the table unfiltered
        self.cardinality = 0

        self.run()

    def output_result(self):
        """Outputs the results in the format needed by DataTables
        """
        output = {}
        output['sEcho'] = str(int(self.request_values['sEcho']))
        output['iTotalRecords'] = str(self.cardinality)
        output['iTotalDisplayRecords'] = str(self.cardinality_filtered)

        output['aaData'] = self.results

        return output

    def run(self):
        """Launch filtering, sorting and paging processes to output results
        """
        # count before filtering
        self.cardinality = self.query.count()

        # the term entered in the datatable's search box
        self.filtering()

        # field chosen to sort on
        self.sorting()

        # pages have a 'start' and 'length' attributes
        self.paging()

        # fetch the result of the queries
        self.results = self.query.all()

        # return formatted results with correct filters applied
        formatted_results = []
        for i in range(len(self.results)):
            row = dict()
            for j in range(len(self.columns)):
                col = self.columns[j]
                tmp_row = get_attr(self.results[i], col.column_name)
                if col.filter:
                    if sys.version_info < (3, 0) \
                            and hasattr(tmp_row, 'encode'):
                        tmp_row = col.filter(tmp_row.encode('utf-8'))
                    tmp_row = col.filter(tmp_row)
                row[col.mData if col.mData else str(j)] = tmp_row
            formatted_results.append(row)

        self.results = formatted_results

    @classmethod
    def prepare_arguments(cls, request):
        request_values = dict()
        for key, value in request.items():
            try:
                request_values[key] = int(value)
            except ValueError:
                if value in ("true", "false"):
                    request_values[key] = value == "true"
                else: # assume string
                    request_values[key] = value
        return request_values

    def filtering(self):
        """Construct the query, by adding filtering(LIKE) on all
        columns when the datatable's search box is used
        """
        search_value = self.request_values.get('sSearch')
        condition = None

        def search(idx, col):
            # TODO: fix for @hybrid properties that reference json or similar
            # columns.
            tmp_column_name = col.column_name.split('.')
            for tmp_name in tmp_column_name:
                # This handles the x.y.z.a option
                if tmp_column_name.index(tmp_name) == 0:
                    obj = getattr(self.sqla_object, tmp_name)
                    parent = self.sqla_object
                elif isinstance(obj.property, RelationshipProperty):
                    # otherwise try and see if we can percolate down the list
                    # for relationships of relationships.
                    parent = obj.property.mapper.class_
                    obj = getattr(parent, tmp_name)

                # Ex: hybrid_property or property
                if not hasattr(obj, 'property'):
                    sqla_obj = parent
                    column_name = tmp_name
                # Ex: ForeignKey
                elif isinstance(obj.property, RelationshipProperty):
                    # Ex: address.description
                    sqla_obj = obj.mapper.class_
                    column_name = tmp_name
                    if not column_name:
                        # find first primary key
                        column_name = obj.property.table.primary_key.columns \
                            .values()[0].name
                else:
                    sqla_obj = parent
                    column_name = tmp_name
            return sqla_obj, column_name

        if search_value:
            conditions = []
            for idx, col in enumerate(self.columns):
                if self.request_values.get('bSearchable_%s' % idx) in (
                        True, 'true') and col.searchable:
                    sqla_obj, column_name = search(idx, col)
                    conditions.append(
                        cast(get_attr(sqla_obj, column_name), String).ilike('%%%s%%' % search_value))
            condition = or_(*conditions)
        conditions = []
        for idx, col in enumerate(self.columns):
            search_value2 = self.request_values.get('sSearch_%s' % idx)

            if search_value2 is not None:

                sqla_obj, column_name = search(idx, col)

                if col.search_like:
                    conditions.append(
                        cast(get_attr(sqla_obj, column_name), String).ilike('%%%s%%' % search_value2))
                else:
                    conditions.append(
                        cast(get_attr(sqla_obj, column_name), String).__eq__(search_value2))

                if condition is not None:
                    condition = and_(condition, and_(*conditions))
                else:
                    condition = and_(*conditions)

        if condition is not None:
            self.query = self.query.filter(condition)
            # count after filtering
            self.cardinality_filtered = self.query.count()
        else:
            self.cardinality_filtered = self.cardinality

    def sorting(self):
        """Construct the query, by adding sorting(ORDER BY) on the
        columns needed to be applied on
        """
        sorting = []

        Order = namedtuple('order', ['name', 'dir'])

        if self.request_values.get('iSortingCols') > 0:

            for i in range(int(self.request_values['iSortingCols'])):
                sorting.append(Order(self.columns[int(self.request_values['iSortCol_' + str(i)])].column_name, self.request_values['sSortDir_' + str(i)]))

        for sort in sorting:
            tmp_sort_name = sort.name.split('.')
            for tmp_name in tmp_sort_name:
                # iterate over the list so we can support things like x.y.z.a
                if tmp_sort_name.index(tmp_name) == 0:
                    obj = getattr(self.sqla_object, tmp_name)
                    parent = self.sqla_object
                elif isinstance(obj.property, RelationshipProperty):
                    # otherwise try and see if we can percolate down the list
                    # for relationships of relationships.
                    parent = obj.property.mapper.class_
                    obj = getattr(parent, tmp_name)

                if not hasattr(obj, "property"):  # hybrid_property or property
                    sort_name = tmp_name
                    if hasattr(parent, "__tablename__"):
                        tablename = parent.__tablename__
                    else:
                        tablename = parent.__table__.name
                # Ex: ForeignKey
                elif isinstance(obj.property, RelationshipProperty):
                    # Ex: address.description => description =>
                    # addresses.description
                    sort_name = tmp_name
                    if not sort_name:
                        # Find first primary key
                        sort_name = obj.property.table.primary_key.columns \
                            .values()[0].name
                    tablename = obj.property.table.name
                else:  # -> ColumnProperty
                    sort_name = tmp_name

                    if hasattr(parent, "__tablename__"):
                        tablename = parent.__tablename__
                    else:
                        tablename = parent.__table__.name

            sort_name = "%s.%s" % (tablename, sort_name)
            self.query = self.query.order_by(
                asc(sort_name) if sort.dir == 'asc' else desc(sort_name))

    def paging(self):
        """Construct the query, by slicing the results in order to
        limit rows showed on the page, and paginate the rest
        """
        pages = namedtuple('pages', ['start', 'length'])

        if (self.request_values['iDisplayStart'] != "") \
                and (self.request_values['iDisplayLength'] != -1):
            pages.start = int(self.request_values['iDisplayStart'])
            pages.length = int(self.request_values['iDisplayLength'])

        offset = pages.start + pages.length
        self.query = self.query.slice(pages.start, offset)