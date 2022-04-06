from websaw import DefaultApp, DefaultContext, redirect
from websaw.core import Fixture
from .models import db
import ombott

from ..mixins import db_admin, auth_mixin

ombott.default_app().setup(dict(debug=True))


# make a simple custom fixture that uses another fixture (session)
class LastVisited(Fixture):
    def take_off(self, ctx: DefaultContext):
        session = ctx.session  # magic goes here - we touch session and ctx activates it!
        last_visited = session.get('last_visited', [])
        last_visited.append(ctx.request.path)
        last_visited = last_visited[-5:]
        session['last_visited'] = last_visited

class DBRegistry(Fixture):
    def __init__(self):
        self.dbs_keys = set()



# extend default context with our fixture and info-mixin context
class Context(db_admin.Context, DefaultContext):
    track_visited = LastVisited()
    db = db
    db_reg = DBRegistry()
    

ctxd = Context()
app = DefaultApp(ctxd, dict(group_name='websaw_apps_group_one'), name=__package__)

# use mixin(s)
app.mixin(db_admin.app, auth_mixin.app)


@app.route('index')
@app.use(ctxd.track_visited, 'index.html')  # note there is no session, but it used!
def index(ctx: Context):
    user = ctx.auth.user
    flash = ctx.flash
    if not user:
        flash.set('Please Sign In in order to access this site', 'danger')
        redirect(ctx.URL('login'))
    if ctx.auth.has_membership('admin'):
        flash.set('Welcom %s . You have admin access so welcome to DB ADMIN' % (ctx.auth.user['email']), 'success')
        redirect(ctx.URL('db_admin'))
    else:
        flash.set('Welcom %s . You do not have admin access so welcome to Index' % (ctx.auth.user['email']), 'success')
    
    return dict(message = 'Hello and Welcome')

