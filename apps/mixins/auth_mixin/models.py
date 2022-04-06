import os
from websaw import DAL, Field, BaseContext
from pydal.validators import *
import datetime
from . import settings
from ..common.widgets import Select2, Dropify

select2 = Select2()
dropify = Dropify()

def get_time():
    fulltime = datetime.datetime.utcnow() 
    stripped = fulltime.strftime('%Y-%m-%d %H:%M:%S')
    print('stripped is ', stripped)
    retval = stripped.replace("T"," ")
    return retval.replace("T"," ")

def get_download_mixin_url(picture):
    ctx = BaseContext.cctx()
    mixin_name = 'auth_mixin' #ctx.mixin_data.app_name
    return ctx.URL(f'static/mxn/{mixin_name}/images/{picture}')

def get_download_url(picture):
    return f"images/{picture}"


class myDAL(DAL):
    def app_mounted(self, ctx):
        db_reg = ctx.ask('db_reg')
        if db_reg:
            self_key = ctx.get_or_make_fixture_key(self)
            db_reg.dbs_keys.add(self_key)

# define database and tables
auth_db = myDAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)

auth_db.define_table("auth_user",
    Field("username", requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(auth_db, "auth_user.username")],
        unique=True, label='Username'
    ),
    Field("first_name", requires=IS_NOT_EMPTY(), label='First Name'),
    Field("last_name",  requires=IS_NOT_EMPTY(), label='Last Name' ),
    Field("sso_id", readable=False, writable=False),
    Field("action_token", readable=False, writable=False),
    Field("last_password_change", "datetime", default=None, readable=False, writable=False),
    Field("email", requires=(IS_EMAIL(), IS_NOT_IN_DB(auth_db, "auth_user.email")),
        unique=True, label='Email'),
    Field("password", "password", requires=CRYPT(),
        readable=False, writable=False, label='Password'),
    Field("past_passwords_hash", "list:string", writable=False, readable=False),
    Field('is_blocked', 'boolean', default=False),
    format='%(email)s'
)
auth_db.auth_user._singular = 'Auth User'
auth_db.auth_user._plural = 'Auth Users'

auth_db.define_table('auth_roles',
                Field('role'),
                Field('description'),
                format='%(role)s')
auth_db.auth_roles._singular = 'Auth Role'
auth_db.auth_roles._plural = 'Auth Roles'

auth_db.define_table('auth_membership',
    Field('user_id', 'reference auth_user', widget=select2.widget),
    Field('role_id', 'reference auth_roles',widget=select2.widget))
auth_db.auth_membership._singular = 'Auth Membership'
auth_db.auth_membership._plural = 'Auth Memberships'

auth_db.define_table(
    "profile",
    Field("user", "reference auth_user", readable=False, writable=False),
    Field("image","upload",
        default="default.jpg",
        uploadfolder=settings.UPLOAD_PATH,
        download_url=get_download_mixin_url, label="Profile Picture", widget=dropify.widget),
    )

def register_profile(field_values, user_id):
    profile = auth_db.auth_user(user_id).profile.select().first()
    if not profile:
        profile = auth_db.profile.insert(user=user_id)

auth_db.auth_user._after_insert.append(register_profile)

auth_db.commit()
