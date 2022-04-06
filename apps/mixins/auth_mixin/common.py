import os
from websaw import DefaultApp, DefaultContext
from websaw.core import Fixture
import ombott
from .. common.fixtures import auth, flash
from .models import auth_db
from . import settings
from PIL import Image
ombott.default_app().setup(dict(debug=True))

def resize_image(image_path):
    total_path = os.path.join(settings.UPLOAD_PATH, image_path)
    img = Image.open(total_path)
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(total_path)


def cleanup_image(image_path):
    total_path = os.path.join(settings.UPLOAD_PATH, image_path)
    print('Inside remove', image_path)
    try:
        os.remove(total_path, dir_fd=None)
    except:
        print('Could not find file to remove', image_path)

# extend default context with our fixture
class DBRegistry(Fixture):
    def __init__(self):
        self.dbs_keys = set()

class Context(DefaultContext):
    auth = auth
    flash=flash
    auth_db = auth_db
    db_reg = DBRegistry()  

ctxd = Context()
app = DefaultApp(ctxd, dict(group_name='websaw_apps_group_one'), name=__package__ )
