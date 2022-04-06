from websaw import DefaultApp, DefaultContext, redirect
from websaw.core import Fixture
from pydal import Field
from ..common.form_1 import Form, FormStyleBulma
import json

class Context(DefaultContext):
    ...
ctxd = Context()
app = DefaultApp(ctxd, name=__package__)

