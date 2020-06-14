from flask import render_template, url_for, flash, redirect,session,Blueprint
from app import db
from app.forms import LoginForm, RegistrationForm, AdminForm, AdminLoginForm, pswForm
from app.models import Users, Admin

login = Blueprint('login', __name__)

@login.before_request
def before_login():
    if 'identity' in session:
        pass
    else:
        session['identity']='Unknown'
        pass

@login.route("/homeAdmin")
def homeAdmin():
    admin = Admin.query.all()
    return render_template('homeAdmin.html', admin=admin)

@login.route("/", methods=['GET', 'POST'])
def a():
    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == Users.name and form.password.data == Users.pwd:
        user = Users.query.filter_by(email=form.email.data, pwd=form.password.data).first()
        print(user)
        if user:
            session['name']=user.username
            session['identity']='user'
            flash('登录成功!','success')
            # db.session['email'] = form.email.data
            return render_template('a.html',title=user.username+'您好',form=form)
        else:
            flash('登录失败！请重新输入账号密码')
    return render_template('a.html', title='Login', form=form)


@login.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = Users.query.filter_by(email=form.email.data).all()
        username = Users.query.filter_by(username=form.username.data).all()
        idc = Users.query.filter_by(idcard=form.idcard.data).all()
        if email:
            flash('该邮箱已被注册过！')
        if username:
            flash('用户名重复！')
        if idc:
            flash('身份证号重复！')
        else:
            user = Users(username=form.username.data, pwd=form.password.data, email=form.email.data,
                         address=form.address.data, name=form.name.data, province=form.province.data,
                         idcard=form.idcard.data, phone=form.phone.data)
            db.session.add(user)
            db.session.commit()
            print(1)
            flash(f'Account created for {form.username.data}!', 'success')
            session['name']=user.username
            return redirect(url_for('login.a'))
    return render_template('register.html', title='Register', form=form)


@login.route("/forget", methods=['GET', 'POST'])
def forget():
    form = pswForm()
    # if form.idcard.data
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data, idcard=form.idcard.data).all()
        print(user)
        if user:
            Users.query.filter_by(idcard=form.idcard.data).update({'pwd':form.password.data})
            flash(f'密码更新成功!', 'success')
            return redirect(url_for('login.a'))
        else:
            flash(f'用户不存在！')
    return render_template('forget.html', title='forget psw', form=form)


@login.route("/adminLog", methods=['GET', 'POST'])
def adminLog():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.name.data, pwd=form.password.data).all()
        if admin:
            session['identity']= admin[0].system
            if 'name' in session:
                session.pop('name')
            flash('登录成功!','success')
            if admin[0].system==1:
                return redirect(url_for('news_admin.index'))
            if admin[0].system==2:
                return redirect(url_for('patient_admin.index'))
            if admin[0].system==3:
                return redirect(url_for('.addAdmin()'))
            if admin[0].system==4:
                return redirect(url_for('transport_admin.index'))
            if admin[0].system==5:
                return redirect(url_for('population_admin.index'))
            if admin[0].system==6:
                return redirect(url_for('supply_admin.index'))
        else:
            flash('登录失败！请重新输入账号密码')
    return render_template('adminLog.html', title='Admin-Login', form=form)


@login.route("/addAdmin", methods=['GET', 'POST'])
def addAdmin():
    form = AdminForm()
    if form.validate_on_submit():
        # admin=Admin(name=form.name.data,pwd=form.password.data)
        admin = Admin(name=form.name.data, pwd=form.password.data, system=form.rights.data)
        print(admin)
        db.session.add(admin)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('login.adminLog'))
    return render_template('addAdmin.html', title='addAdmin', form=form)
