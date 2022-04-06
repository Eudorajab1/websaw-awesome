# Main App

This is a minimal app to demonstrate the use of mixins in Websaw.

The Main app defines its own database as well as uses the database defined in the auth_mixin but from then on mainly uses the mixins

This App has just one action ... index which uses the auth_mixin to see if a user is admin or not.

If the user is admin we redirect to db_admin (which is the other mixin) all from within the same app

At the same time the main app has access to all the actions defined in the mixins.

Pretty cool if you ask me!!

## Auth_mixin
The auth_mixin is responsible for login, logout, register and profiles and holds all the tables necessary for simple auth managements. 

## Db_admin mixin

The db_admin mixin (provided you have admin rights) will allow you to look at all tables and do normal CRUD admin tasks.

## Common folder

Added this just to store files common to mixins. Things like forms, widgets, fixtures etc.

### Notes

You will see that the db_admin mixin has access to both the auth_db (defined in the auth_mixin) as well as db (defined in the main app)

The db_admin mixin is completely db agnostic and will work wiht all databases at all levels.

### Usage

For admin access login as username: admin password: admin

For user access login as username: user password: user.


