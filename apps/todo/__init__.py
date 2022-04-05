import os
from websaw import DefaultContext, DefaultApp, DAL, Cache, Field, HTTP
from websaw.core import Fixture

# define session and cache objects
cache = Cache(size=1000)


# define database and tables
db = DAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)
db.define_table(
    "todo",
    Field("info"),
    Field("counter", default=(lambda: mounted_ctx.session['counter']))
)
db.commit()


# make logged session fixture
class UserIn(Fixture):
    def take_on(self, ctx: 'Context'):
        if not ('user' in ctx.session and ctx.session['user']['id']):
            raise HTTP(401, body='Sorry')


class Context(DefaultContext):
    db = db
    user_in = UserIn()


ctx_ = Context()

app = DefaultApp(ctx_, name=__package__)


# example index page using session, template and vue.js
@app.route("index")  # the function below is exposed as a GET action
@app.use("index.html")  # we use the template index.html to render it
def index(ctx: Context):
    session = ctx.session
    session["counter"] = session.get("counter", 0) + 1
    session["user"] = {"id": 1}  # store a user in session
    return dict(session=session)


# example of GET/POST/DELETE RESTful APIs

@app.route("api")  # a GET API function
def todo(ctx: Context):
    db = ctx.db
    return dict(items=db(db.todo).select(orderby=~db.todo.id).as_list())


@app.route("api", method="POST")
@app.use(ctx_.user_in)
def todo(ctx: Context):
    request = ctx.request
    db = ctx.db
    return dict(id=db.todo.insert(info=request.json.get("info")))


@app.route("api/<id:int>", method="DELETE")
@app.use(ctx_.user_in)
def todo(ctx: Context, id):
    db = ctx.db
    db(db.todo.id == id).delete()
    return dict()


# example of caching
@app.route("uuid")
@cache.memoize(expiration=5)  # here we cache the result for 5 seconds
def uuid(ctx: Context):
    import uuid
    return str(uuid.uuid4())


# mounted_ctx could be used as global object to get/store some data
# e.g. like above:  Field("counter", default=(lambda: mounted_ctx.session['counter']))
# but it is bad practice
app.mount()
# instaed of that you can:
#class DBDefs(Fixture):
#    def take_on(self, ctx: 'Context'):
#        db = ctx.db
#        db.table.field.default = (lambda: ctx.session['counter'])
#
#class Context(DefaultContext):
#     ...
#     db_defs = DBDefs()
#
#@app.use(ctx_.db_defs)

