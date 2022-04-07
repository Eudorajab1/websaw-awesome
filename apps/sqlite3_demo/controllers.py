import sqlite3

from websaw import DefaultApp, DefaultContext, Reloader, HTTP
from websaw.core import Fixture

from .app_fixtures import SQLite3

sqlite_db = Reloader.package_folder_path(__package__,  'demo_db.sqlite')

# lets create the table in our db
def init_db(sqlite_db):
    db = sqlite3.connect(sqlite_db)
    db.execute('CREATE TABLE IF NOT EXISTS thing(id INTEGER PRIMARY KEY, name TEXT)')

init_db(sqlite_db)


# extend default context with our fixture
class Context(DefaultContext):
    # to get right autocomplete in action (e.g. when ctx.sdb.exe...)
    # we need to force IDE to think that cxt.sdb is type of sqlite3.Connection
    sdb: sqlite3.Connection = SQLite3(sqlite_db)

ctxd = Context()
app = DefaultApp(ctxd, name=__package__)

@app.route('sdb')
def sdb(ctx: Context):
    q = ctx.request.query
    action = q.get('action')
    if not action:
        cur = ctx.sdb.execute('SELECT * FROM thing')
        ret = [{**r} for r in cur.fetchall()]
    elif action == 'create':
        name = q.get('name')
        if not name:
            raise HTTP(429, 'Name is required')
        cur = ctx.sdb.execute('INSERT INTO thing(name) values(?)', (name,))
        ret = cur.lastrowid
    else:
        raise HTTP(400, f'Unkown action: {action}')
    return dict(result=ret)

# to insert any name into db
#http://127.0.0.1:8000/sqlite3_demo/sdb?action=create&name=John

# to view all rows in db
#http://127.0.0.1:8000/sqlite3_demo/sdb