import os
from websaw import DefaultApp, DefaultContext, Reloader

pjoin = os.path.join


class Context(DefaultContext):
    env = {
        'mixin_env': 'mixin env is not mixed-in since it is not secure',
        'templ_dir': Reloader.package_folder_path(__package__, 'templates')
    }
    ...


ctx_ = Context()
app = DefaultApp(ctx_, name=__package__)


# To make template replaceable/referenceable we should assign a fixture key (e.g. welcome_templ)
# To do that use the following syntax for template:
# '<fixture_key>:<template.html>'
@app.route('welcome')
@app.use('welcome_templ:welcome.html')
def welcome(ctx):
    msg = (
        'Hey! this is message from info-mixin cntroller'
        'It uses mixin template'
    )
    return dict(msg=msg)


@app.route('welcome_template_overwritten')
@app.use('welcome_templ_overwrite:welcome.html')
def welcome_overwite_template(ctx):
    msg = (
        'Hey! this is message from info-mixin cntroller '
        'It uses named template `welcome_templ_overwrite` '
        'which could be overwritten by app context (like this one)'
    )
    return dict(msg=msg)


@app.route('welcome_template_from_env')
@app.use('{templ_dir}/welcome.html')
def welcome_template_env(ctx):
    msg = (
        'Hey! this is message from info-mixin cntroller '
        "It uses template `welcome.html` from ctx.env['templ_dir'] "
    )
    return dict(msg=msg)


@app.route('info/app')
def info_app(ctx: Context):
    def rep(v):
        if isinstance(v, list):
            return [rep(_) for _ in v]
        if isinstance(v, str):
            return v
        return repr(v)

    ret = {
        k: rep(v) for k, v in ctx.app_data.__dict__.items()
    }
    ret['env'] = ctx.env
    return ret
