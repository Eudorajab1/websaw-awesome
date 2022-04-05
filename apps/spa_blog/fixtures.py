from websaw import DefaultApp, DefaultContext, XAuth, AuthErr, redirect
from websaw.core import request, Fixture, BaseContext
from pprint import pprint
class Auth(XAuth):
    def take_on(self, ctx: BaseContext):
        self.data.ctx = ctx
        self.data.db = ctx.db
        self.data.session = ctx.session
        self.data.cuser = ctx.current_user
        self.data.user = self.data.cuser.user
        self.data.shared_data = ctx.state.shared_data
        if not self.data.shared_data.get('template_context', None):
            self.data.shared_data['template_context'] = {} #intialise it 
        self.data.shared_data['template_context']['auth_user'] = self.data.cuser.user
        
        flash = self.data.session.get('message', None)
        if flash:
            f_message = dict(message=flash['message'], _class=flash['_class'])
            self.data.shared_data['template_context']['flash'] = f_message
            self.data.session['message'] = None
        
    def user_by_login(self, login: str) -> dict:
        login = login.lower()
        db = self.data.db
        user = db(db.auth_user.username == login).select().first()
        return user
        
    def user_for_session(self, user):
        suser = super().user_for_session(user)
        suser['email'] = user['email']
        suser['username'] = user['username']
        suser['first_name'] = user['first_name']
        suser['last_name'] = user['last_name']
        return suser

    def register(self, fields):
        db = self.data.db
        pwd_crypt = self.crypt(fields['password'])
        fields['password'] = pwd_crypt
        ret = db.auth_user.insert(**fields)
        db.commit()
        return ret

    def update_profile(self, user_id, fields):
        db = self.data.ctx.auth_db
        res = db.auth_user(user_id).update_record(
            username = fields["username"],
            email = fields["email"],
            first_name = fields["first_name"],
            last_name = fields["last_name"],
        )
        db.commit()
        print('Res in update_profiel is ', res)
        if res:
            self.store_user_in_session(res.as_dict())
            return res['id']
        else:
            return dict(message='Could not update profiel', _class='danger')    

    def has_membership(self, role):
        user_id = self.user_id
        db = self.data.db
        belongs = db(db.auth_membership.user_id == user_id).select()
        for b in belongs:
            if db.auth_roles(b.role_id).role == role:
                return True
        return False

auth = Auth()

