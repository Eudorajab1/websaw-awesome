from websaw import DefaultApp, redirect, Reloader
from websaw.core import Fixture
from pydal import Field
from ..common.form_1 import Form, FormStyleBulma
from .common import Context, ctxd, cleanup_image, resize_image
import json

app = DefaultApp(ctxd, name=__package__)

@app.route('auth_index', method=['GET', 'POST'])
@app.use('index.html')
def index(ctx: Context):
    user = ctx.auth.user
    flash = ctx.flash
    
    if not user:
        flash.set('Please Sign In in order to access this site', 'danger')
        redirect(ctx.URL('login'))
    if not ctx.auth.has_membership('admin'):
        flash.set('You do NOT have Admin access rights !!!', 'danger')
    else:
        flash.set('Welcome %s %s you are logged in as Admin' % (user['first_name'], user['last_name']), 'success')
        redirect(ctx.URL('db_admin'))    
    return dict(user=user)


@app.route('login', method=['GET', 'POST'])
@app.use('login.html')
def login(ctx):
    user = ctx.auth.user
    db = ctx.ask('auth_db')
    flash = ctx.flash

    form_list = [(Field('username')), (Field('password', 'password'))]
    # We will use a list of fields here as the password field is readonly in the db

    form = Form(ctx, form_list, dbio=False, formstyle=FormStyleBulma)
    if form.accepted:
        user, autherr = ctx.auth.login(form.vars['username'], form.vars['password'] )
        if user:
            flash.set('Welcome %s %s you are welcome here' % (user['first_name'], user['last_name']), 'success')
            redirect(ctx.URL('index'))
        else:
            flash.set('Hey %s !!!!! Not so cool..... We have no idea who you are!!!!' % (form.vars['username']), 'danger')
    return dict(form=form)


@app.route('logout', method=['GET', 'POST'])
def logout(ctx: Context):
    flash = ctx.flash
    user = ctx.auth.user
    flash.set('You have now logged out .. see you again soon ', 'info')
    ctx.auth.logout()
    redirect(ctx.URL('login'))

@app.route('register', method=['GET', 'POST'])
@app.use('register.html')
def register(ctx: Context):
    q = ctx.request.query
    db = ctx.ask('auth_db')
    flash = ctx.flash
    user = ctx.auth.user
    form_list = [field for field in db.auth_user if not field.type == "id" and not field.name =="is_blocked"] + [
        (Field('password', 'password')), (Field('password_again', 'password'))]
    aform = Form(ctx,
        form_list,
        dbio=False,
        formstyle=FormStyleBulma,
    )
    if aform.accepted:
        if aform.vars['password'] == aform.vars['password_again']:
            aform.vars['password'] = ctx.auth.crypt(aform.vars['password']) # crypt it here 
            res = ctx.auth.register(aform.vars)
            if res: 
                flash.set('Registration successfull', 'success')
                redirect(ctx.URL('login'))
            else:
                flash.set('Registration not soo good', 'danger')
        else:
            flash.set('Passwords do not match. Please type carefully', 'warning')          
    
    elif aform.errors:
        print('Errors', json.dumps(aform.errors))
        flash.set('Form has errors  %s' % json.dumps(aform.errors), 'danger')
    return dict(aform=aform)

@app.route('profile', method=['GET', 'POST'])
@app.use('profile.html')
def profile(ctx: Context):
    user = ctx.auth.user
    q = ctx.request.query
    db = ctx.ask('auth_db')
    flash = ctx.flash
    profile = db.auth_user(user['id']).profile.select().first()
    if not profile:
        db.profile.insert(user=ctx.auth.user['id'], image='default.jpeg')
    
    profile = db.auth_user(user['id']).profile.select().first()
    icon = ctx.URL('static/mxn', ctx.mixin_data.app_name, f"images/{profile.image}")
    
    # Append the user profile icon to the dict so it prepopulates it with current data
    user.update({"image": profile.image})

    # Get all the required fields out of the 2 tables to display them: Username, Email, First/Last name, and Profile Pic
    form_list = [field for field in db.auth_user if not field.type == "id" and field.name!='is_blocked'] + [
        field for field in db.profile if not field.type == "id"
    ]
    aform = Form(ctx,
        form_list,
        record=user,
        deletable=False,
        formstyle=FormStyleBulma,
    )
    if aform.accepted:
        # Update the auth user
        res = ctx.auth.update_profile(user['id'], aform.vars)
        # The icon we want to update our profile will always have a default of default.jpg
        update_icon = "default.jpg"

        if not aform.vars["image"] and profile.image == update_icon:
            # We can't delete the default image so we just redirect back to the page.
            print('Inside not aform vars and profileimage == default')
            redirect(ctx.URL("profile"))

        if aform.vars["image"]:
            # If we are setting it equal to a new icon, we set icon to that file name
            update_icon = aform.vars["image"]

        if update_icon != profile.image:
            # If the new icon (which can be default.jpg) isn't the same icon as before, remove the old one and update
            if profile.image != "default.jpg":
                cleanup_image(profile.image)
                resize_image(update_icon)
            profile.update_record(image=update_icon)
            db.commit()
        # Once done with everything (Or after doing nothing because the icons are the same), return to the profile page
        ctx.flash.set('Congratulation you have updated your profile', 'info')
        redirect(ctx.URL("profile"))
    return dict(icon=icon, aform=aform)
