from sqlalchemy.engine import default
from sqlalchemy.engine import reflection
from sqlalchemy import types

_type_map = {
    4  : types.Integer,
    -5 : types.BigInteger,
    9  : types.Integer,
    10 : types.BigInteger,
    -6 : types.SmallInteger,
    11 : types.SmallInteger,
    5  : types.SmallInteger,
    13 : types.SmallInteger,
    6  : types.Float,
    14 : types.Float,
    8  : types.Float,
    15 : types.Float,
    3  : types.DECIMAL,
    16 : types.Boolean,
    92 : types.Time,
    91 : types.Date,
    93 : types.TIMESTAMP,
    18 : types.Time,
    19 : types.Date,
    20 : types.TIMESTAMP,
    12 : types.String,
    1  : types.String,
    -2 : types.String,
    -3 : types.String
}

class PhoenixDialect(default.DefaultDialect):
    # default_paramstyle = 'qmark'
    name = 'phoenix'

    def __init__(self, **kwargs):
        super(PhoenixDialect, self).__init__(**kwargs)

    @classmethod
    def dbapi(cls):
        from pyphoenix import phoenix
        return phoenix

    def get_schema_names(self, connection, **kw):
        schema_query = 'select table_schem from SYSTEM.CATALOG group by table_schem'
        result = connection.execute(schema_query)
        return [row[0] for row in result if row[0]]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        where = ("where table_schem='%s'" % schema) if schema else 'where table_schem is null'
        tables_query = 'select table_name from SYSTEM.CATALOG %s group by table_name' % where
        result = connection.execute(tables_query)
        return [row[0] for row in result]

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_unique_constraints(self, connection, table_name,
                               schema=None, **kw):
        return []

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        where = ("where table_schem='%s'" % schema) if schema else 'where table_schem is null'
        where += " and table_name='%s' and column_name is not null" % table_name
        columns_query = 'select column_name, data_type from SYSTEM.CATALOG %s' % where
        result = connection.execute(columns_query)
        ret = []
        for row in result:
            _type = _type_map.get(row[1])
            if _type:
                ret.append({'default': None, 'autoincrement': False, 'type': _type, 'name': row[0], 'nullable': False})
        return ret

dialect = PhoenixDialect
