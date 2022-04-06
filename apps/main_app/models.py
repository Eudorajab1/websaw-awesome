import os
from websaw import DAL, Field
from pydal.validators import *
import datetime
from . import settings

def get_time():
    fulltime = datetime.datetime.utcnow() 
    stripped = fulltime.strftime('%Y-%m-%d %H:%M:%S')
    print('stripped is ', stripped)
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

db = myDAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)
db.define_table(
    "owner",
    Field('user_id'),
    Field('name')
)
db.owner._singular = 'Owner'
db.owner._plural = 'Owners'

db.define_table(
    "things",
    Field('thing_id'),
    Field('name')
)
db.things._singular = 'Thing'
db.things._plural = 'Things'

db.commit()

