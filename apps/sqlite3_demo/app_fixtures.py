import sqlite3
from websaw import DefaultContext

from websaw.core import Fixture

class SQLite3(Fixture):
    def __init__(self, uri_or_fpath, **kwargs):
        self.uri_or_fpath = uri_or_fpath
        self.kwargs = kwargs

    def take_on(self, ctx):
        # self.data - thread safe local storage
        conn = self.data.db = sqlite3.connect(self.uri_or_fpath, **self.kwargs)
        conn.row_factory = sqlite3.Row
        return conn

    def take_off(self, ctx: DefaultContext):
        db: sqlite3.Connection = self.data.db
        if ctx.exception:
            # there is some error(s) during action processing or/and
            # in other fixtures, so we don't want to save changes
            db.rollback()
        else:
            db.commit()
        db.close()