import os
from .voodoodal import DB, Table, Field, model
from websaw import DAL, BaseContext
from pydal.validators import *
import datetime

def get_time():
    fulltime = datetime.datetime.utcnow() 
    stripped = fulltime.strftime('%Y-%m-%d %H:%M:%S')
    retval = stripped.replace("T"," ")
    return retval.replace("T"," ")

def get_download_url(picture):
    return f"images/{picture}"

class myDAL(DAL):
    def app_mounted(self, ctx):
        db_reg = ctx.ask('db_reg')
        if db_reg:
            self_key = ctx.get_or_make_fixture_key(self)
            db_reg.dbs_keys.add(self_key)

_db = myDAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)
model = model(_db)

def get_user_email():
    return BaseContext.cctx().current_user.user.get('email', None)

class sign_created(Table):
    created = Field('datetime', default = get_time)
    created_by = Field(default = get_user_email)
    

class sign_updated(Table):
    updated = Field('datetime', default = get_time)
    updated_by = Field(default = get_user_email)

@model
class db(DB):
    class room(Table):
        name = Field()
        format = '%(name)s'
        singular = 'Room'
        plural = 'Roooms'

"""    
        @property
        def owner_thing_ids(row):
            # This will turn into `Field.Virtual`
            return (row.thing.owner, row.thing.id)
"""
db.commit()

