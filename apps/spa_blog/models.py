"""
This file defines the database models
"""

import os
from websaw import DAL, Field, BaseContext
from pydal.validators import *
import datetime
from . import settings

def get_time():
    return datetime.datetime.utcnow()

def get_download_url(picture):
    return f"images/{picture}"

def get_current_user():
    ctx = BaseContext.cctx()
    return ctx.current_user.user['id']
    

class myDAL(DAL):
    def app_mounted(self, ctx):
        db_reg = ctx.ask('db_reg')
        if db_reg:
            self_key = ctx.get_or_make_fixture_key(self)
            db_reg.dbs_keys.add(self_key)
    
# define database and tables
db = myDAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)
db.define_table("auth_user",
    Field("username", requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db, "auth_user.username")],
        unique=True, label='Username'
    ),
    Field("first_name", requires=IS_NOT_EMPTY(), label='First Name'),
    Field("last_name",  requires=IS_NOT_EMPTY(), label='Last Name' ),
    Field("sso_id", readable=False, writable=False),
    Field("action_token", readable=False, writable=False),
    Field("last_password_change", "datetime", default=None, readable=False, writable=False),
    Field("email", requires=(IS_EMAIL(), IS_NOT_IN_DB(db, "auth_user.email")),
        unique=True, label='Email'),
    Field("password", "password", requires=CRYPT(),
        readable=False, writable=False, label='Password'),
    Field("past_passwords_hash", "list:string", writable=False, readable=False),
    Field('is_blocked', 'boolean', default=False),
    format='%(email)s'
)
db.auth_user._singular = 'Auth User'
db.auth_user._plural = 'Auth Users'

db.define_table(
    "post",
    Field("title", "string", requires=IS_NOT_EMPTY()),
    Field("content", "text", requires=IS_NOT_EMPTY()),
    Field("date_posted", "datetime", default=get_time, readable=False, writable=False),
    Field(
        "author",
        "reference auth_user",
        #default=get_current_user,
        readable=False,
        writable=False,
    ),
)

db.define_table(
    "profile",
    Field("user", "reference auth_user", readable=False, writable=False),
    Field(
        "image",
        "upload",
        requires = IS_EMPTY_OR(IS_FILE()),
        default="",
        uploadfolder=settings.UPLOAD_PATH,
        download_url=get_download_url, label="Profile Picture",
    ),
)
# We do not want these fields to appear in forms by default.
db.post.id.readable = False
db.post.id.writable = False
db.profile.id.readable = False
db.profile.id.writable = False

def register_profile(field_values, user_id):
    profile = db.auth_user(user_id).profile.select().first()
    if not profile:
        profile = db.profile.insert(user=user_id)

db.auth_user._after_insert.append(register_profile)

db.commit()
