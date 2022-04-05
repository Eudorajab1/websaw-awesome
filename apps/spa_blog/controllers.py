import os
from websaw import DefaultApp, DefaultContext, HTTP, URL
from websaw.core import Fixture
import ombott
from .fixtures import auth
from .models import db
from .common import app, ctxd, Context
from . import settings
from PIL import Image
from .spa_form import Form as SPAForm
import json

ombott.default_app().setup(dict(debug=True))


def action_agg(*path_list):
    def inner(f):
        plist = reversed(path_list)
        ret = app.route(next(plist))(f)
        for p in plist:
            ret = app.route(p)(ret)
        return ret
    return inner


class APIError(HTTP):
    def __init__(self, code, body = ''):
        basis = super()
        basis.__init__(code, type=basis.Type.error)
        self._body = body

    @property
    def body(self):
        ret = self._body
        if isinstance(ret, dict):
            ret = json.dumps(self._body, ensure_ascii=False)
        return ret

def profile_get(user):
    user = user
    db = DefaultContext.cctx().db
    profile = db.auth_user(user.get('id')).profile.select().first()
    if not profile: 
    # for some reason we dont have a profile for this user
        db.profile.insert(user_id=user['id'])
        profile = db.auth_user(user["id"]).profile.select().first()
    # Append the user profile icon to the dict so it prepopulates it with current data
    #profile["user_id"] = user["id"]
    user.update(dict(
        image = profile.image,
        profile_id = profile.id,
        user_id = user["id"]
    ))
    #JAB why !!!!del user['id']
    return user

@action_agg('index', 'home', 'about', 'login','register', 'profile', 'post', 'post/<pid:int>', 'post/new', 'post/user/<uid:int>')
@app.use("index.html")
def index(ctx: Context, pid = None, uid = None):
    return dict(app_root = str(ctx.URL()), title = 'blog')

@app.route("auth/api/register", method='POST')
def login(ctx: Context):
    form = ctx.request.json
    if form:
        res = ctx.auth.register(form)
    return dict()

@app.route("auth/api/login", method='POST')
def login(ctx: Context):
    form = ctx.request.json
    if form:
        user, autherr = ctx.auth.login(form['username'], form['password'] )
        if user:
            r_user = dict(id=user.get('id'), username=user.get('username'))
            return dict(user=r_user)
        else:
            user = ctx.current_user.user
        return dict(user=user)
    else:
        return
@app.route("auth/api/logout", method='POST')
def login(ctx: Context):
    ctx.auth.logout()
    return dict(user=None)

@app.route("auth/api/change_password", method='POST')
def login(ctx: Context):
    print('Inside auth/ašpi/change_password')
    form = ctx.request.json
    if form:
        ctx.auth.change_password(form)
    return dict()

@app.route('try_connect')
@app.use(ctxd.auth_guard)
def try_connect(ctx: Context):
    user = ctx.current_user.user
    return dict(user = user)

def post_get(pid = None, uid = None):
    ctx = DefaultContext.cctx()
    db = ctx.db
    q = db.post.author == db.auth_user.id
    q &= db.profile.user == db.auth_user.id
    if pid:
        q &= db.post.id == pid
    elif uid:
        q &= db.post.author == uid
    rows = db(q).select(db.post.ALL, db.profile.image, db.auth_user.username)
    plist = []
    for r in rows:
        r.post.update(date_posted = str(r.post['date_posted'])) ## json doesnt like datetime objects
        rec = r.post
        rec.author_icon = r.profile.image
        rec.username = r.auth_user.username
        plist.append(rec.as_dict())
    return plist

def post_del(pid):
    ctx = DefaultContext.cctx()
    rec = ctx.db.post(pid)
    if not rec:
        raise APIError(404)
    if rec.author != ctx.current_user.user['id']:
        raise APIError(403)
    rec.delete_record()
    return dict()

@app.route("api_blog/post")
@app.route("api_blog/post/user/<uid:int>")
@app.route("api_blog/post/<pid:int>")
def post(ctx: Context, pid = None, uid = None):
    return dict(items = post_get(pid, uid))

@app.route("api_blog/post", method = ['POST'])
@app.route("api_blog/post/<pid:int>", method = ['PUT', 'DELETE'])
def post_cud(ctx: Context, pid = None):
    db = ctx.db
    user = ctx.auth.user
    if ctx.request.method == 'DELETE':
        return post_del(pid)

    rec = None
    if pid:
        rec = db.post(pid)
        if not rec:
            raise APIError(404)
        if rec.author != user['id']:
            raise APIError(403)

    form = SPAForm(db.post)
    if form(ctx.request.json or ctx.request.POST, record_id = rec and rec.id).accepted:
        if not rec:
            db.post.author.default = user['id']
            pid = form.insert(db.post)
        else:
            form.update(record = rec)
        return dict(items = post_get(pid))
    raise APIError(422, dict(errors= form.errors))

@app.route("api_blog/profile", method = ['GET', 'PUT'])
def profile(ctx: Context):
    
    db = ctx.db
    user = ctx.session.get('user')
    profile = profile_get(user)
    if ctx.request.method == 'GET':
        return dict(profile = profile)

    form_list = [field for field in db.auth_user if field.writable] + [
        field for field in db.profile if field.writable
    ]

    form = SPAForm(form_list)
    user_id = profile['user_id']
    if form(ctx.request.json or ctx.request.POST, record_id = user_id).accepted:
        form.upload()
        form.update(db.auth_user, record_id = user_id)
        form.update(db.profile, record_id = profile['profile_id'], del_files = True)
        update_icon = form.vars.get('image')
        if update_icon:
            resize_image(update_icon)
        s_user = ctx.current_user.user
        return dict(profile = profile_get(s_user))
    raise APIError(422, dict(errors= form.errors))


def resize_image(image_path):
    total_path = os.path.join(settings.UPLOAD_PATH, image_path)

    img = Image.open(total_path)
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(total_path)

