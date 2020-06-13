from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import LoginForm, RegistrationForm, AdminForm, AdminLoginForm, pswForm
from app import db


class Permission:
    FOLLOW = 0X01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x03


'''

class Role(db.Model):
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            'Admin': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
        '''


class Users(db.Model):
    __tablename__ = 'user'
    name = db.Column(db.String(40), unique=True, nullable=False)
    pwd = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(50), unique=True, index=True)
    idcard = db.Column(db.String(20), unique=True, index=True,primary_key=True)
    address = db.Column(db.String(100), unique=True, index=True)
    province = db.Column(db.String(10), unique=True, index=True)
    username = db.Column(db.String(20), unique=True, index=True)

    def __init__(self, name, pwd, phone, email, idcard, address, province,username):
        self.name = name
        self.pwd = pwd
        self.phone = phone
        self.email = email
        self.idcard = idcard
        self.address = address
        self.province = province
        self.username=username

    def verify_password(self, password):
        return check_password_hash(generate_password_hash(self.pwd), password)

    def __repr__(self):
        return "%s/%s/%s/%s/%s/%s" % (
            self.name, self.pwd, self.phone, self.email, self.idcard, self.address)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    pwd = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, index=True)
    province = db.Column(db.String(150), nullable=True)
    auth = db.Column(db.Integer, unique=True, nullable=True)
    system = db.Column(db.Integer, unique=True, nullable=False)

    def is_admin(self):
        '''检查是否为管理员'''
        return self.can(Permission.ADMINISTER)

    def get_id(self):
        return str(self.id)

    def verify_password(self, password):
        return check_password_hash(generate_password_hash(self.pwd), password)



    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


def register():
    name = RegistrationForm.name.data
    pwd = RegistrationForm.password.data
    phone = RegistrationForm.phone.data
    email = RegistrationForm.email.data
    idcard = RegistrationForm.idcard.data
    address = RegistrationForm.address.data
    user = Users(name, pwd, phone, email, idcard, address)
    db.session.add(user)
    db.session.commit()


def add():
    admin = Admin(name=AdminForm.name.data, pwd=AdminForm.password.data,system=AdminForm.rights.data)
    db.session.add(admin)
    db.session.commit()


'''
@LoginManager.user_loader
def load_user(id):
    return Users.query.get(int(id))

'''
