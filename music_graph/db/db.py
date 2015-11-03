from collections import namedtuple

import sqlite3


class MultipleMatchingRows(Exception):
    pass


class NoMatchingRows(Exception):
    pass


class Table(object):
    name = None

    def __init__(self, name, database_uri):
        self.name = name
        self.conn = sqlite3.connect(database_uri)
        self.conn.row_factory = namedtuple_row_factory

    def commit(self):
        self.conn.commit()

    def execute(self, *args):
        return self.conn.execute(*args)

    def executemany(self, *args):
        return self.conn.executemany(*args)

    def insert(self, **kwargs):
        columns, values = zip(*kwargs.items())
        sql = "INSERT INTO %s(%s) VALUES (%s);" % (
            self.name,
            ', '.join(columns),
            ', '.join(['?'] * len(columns)))
        self.execute(sql, values)
        self.commit()

    def insertmany(self, columns, values):
        sql = "INSERT INTO %s(%s) VALUES (%s);" % (
            self.name,
            ', '.join(columns),
            ', '.join(['?'] * len(columns)))
        self.executemany(sql, values)
        self.commit()

    def select(self, **kwargs):
        sql = "SELECT * FROM %s" % self.name
        if kwargs:
            columns, values = zip(*kwargs.items())
            conditions = ' AND '.join('%s = ?' % column
                                  for column in columns)
            sql += " WHERE %s" % (conditions,)
        else:
            values = []
        sql += ";"
        return self.execute(sql, values)

    def select_unique(self, **kwargs):
        rows = list(self.select(**kwargs))
        if not rows:
            raise NoMatchingRows()
        elif len(rows) == 1:
            return rows[0]
        else:
            raise MultipleMatchingRows()

    def select_unique_or_insert(self, **kwargs):
        try:
            return self.select_unique(**kwargs)
        except NoMatchingRows:
            self.insert(**kwargs)
            return self.select_unique(**kwargs)


def namedtuple_row_factory(cursor, row):
    columns = [col[0] for col in cursor.description]
    Row = namedtuple("Row", columns)
    return Row(*row)
