from flask import render_template, url_for,redirect, Blueprint,session,flash,request
from app import db
from app.transportation_models import  USER,Transport
from sqlalchemy import text

transport_user = Blueprint('transport_user', __name__)

@transport_user.before_request
def before_user():
    if 'identity' in session and session['identity']==4:
        return redirect(url_for('transport_admin.index'))
    else:
        pass

@transport_user.route("/", methods=['GET', 'POST'])
def index():
    name = session.get('name')
    if (name is None):
        name = ""
    print(name)
    transport0 = Transport.query.filter_by(type=0)
    transport1=Transport.query.filter_by(type=1)
    if(session.get('name') is None and 'transport_number' in session):
        session.pop('transport_number')

    return render_template('transportation.html', transport0=transport0, name=name,transport1=transport1)


@transport_user.route('/search', methods=['GET', 'POST'])
def turnsearch():
    if 'identity' in session and session['identity']=='Unknown':
        flash('请先登录！','warning')
        return redirect(url_for('.index'))
    if 'identity_number' in session:
        return render_template('search.html')
    else:
        flash('您还未填写个人信息，无法搜索，请先填写个人信息！','warning')
        print('您还未注册个人信息！')
        return render_template('msg_input.html')


@transport_user.route('/results', methods=['GET', 'POST'])
def turnresult():
    if 'identity' in session and session['identity']=='Unknown':
        flash('请先登录！','warning')
        return redirect(url_for('.index'))
    if(session.get('name') is None and 'transport_number' in session):
        session.pop('transport_number')
    return render_template('results.html')


@transport_user.route('/msg_input', methods=['GET', 'POST'])
def turninput():
    if 'identity' in session and session['identity']=='Unknown':
        flash('请先登录！','warning')
        return redirect(url_for('.index'))
    if(session.get('name') is None and 'transport_number' in session):
        session.pop('transport_number')
    return render_template('msg_input.html')


@transport_user.route('/indexregister/<number>', methods=['GET', 'POST'])
def indexregister(number):
    session['transport_number'] = number
    if 'identity_number' in session:
        return redirect(url_for('transport_user.searchregister', number=session['transport_number']))
    return redirect(url_for('transport_user.msg_input'))

@transport_user.route('/register', methods=['GET', 'POST'])
def msg_input():
    if 'identity' in session and session['identity']=='Unknown':
        flash('请先登录！','warning')
        return redirect(url_for('.index'))
    if request.method == 'POST':
        if 'transport_number' in session:
            name = request.form['name']
            identity_number = request.form['identity_number']
            address = request.form['address']
            phone_number = request.form['phone_number']
            email = request.form['email']
            session['identity_number'] = identity_number
            session['address'] = address
            session['phone_number'] = phone_number
            session['email'] = email
            q_user = USER.query.filter_by(idcard=identity_number).first()
            if (q_user):
                flash('您已填写信息！','info')
                print('您已填写信息！')
                return redirect(url_for('transport_user.turnsearch'))
            else:
                try:
                    new_user = USER(name=name, identity_number=identity_number, email=email, address=address,
                                    phone_number=phone_number,transport_number=session['transport_number'])
                    db.session.add(new_user)
                    db.session.commit()
                    flash('登记成功！','success')
                    print('登记成功！')
                    return redirect(url_for('transport_user.index'))
                except Exception as e:
                    print(e)
                    flash('添加出错','danger')
                    db.session.rollback()
        else:
            name = request.form['name']
            print(name)
            identity_number = request.form['identity_number']
            address = request.form['address']
            phone_number = request.form['phone_number']
            email = request.form['email']
            session['identity_number'] = identity_number
            session['address'] = address
            session['phone_number'] = phone_number
            session['email'] = email
            q_user = USER.query.filter_by(identity_number=identity_number).first()
            if (q_user):
                if (q_user.transport_number):
                    flash('您已填写信息！','info')
                    return render_template('msg_input.html')
            else:
                try:
                    new_user = USER(name=name, identity_number=identity_number, email=email, address=address,
                                    phone_number=phone_number)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('填写成功！','success')
                    return render_template('search.html')
                except Exception as e:
                    print(e)
                    flash('添加出错','danger')
                    db.session.rollback()
    return render_template('msg_input.html')


@transport_user.route('/searchtransport', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        type = request.form['type']
        start = request.form['start']
        end = request.form['end']
        time = request.form['time']
        session['type']=type
        session['start']=start
        session['end']=end
        session['time']=time
        if (type == "" and start == "" and end == "" and time == ""):
            flash("请输入查询条件！",'warning')
            return redirect(url_for('transport_user.turnsearch'))
        q_transport = Transport.query.filter(
            Transport.type.like(type+"%") if type is not None else text(''),
            Transport.start.like(start+"%") if start is not None else text(''),
            Transport.end.like(end+"%") if end is not None else text(''),
            Transport.time.like(time+"%") if time is not None else text('')
        ).all()
        if (q_transport):
            # session['q_transport']=q_transport
            return render_template('results.html', transport=q_transport)
        else:
            flash('数据库中无该条件班次！','warning')
    return render_template('search.html')


@transport_user.route('/searchregist/<number>', methods=['GET', 'POST'])
def searchregister(number):
    identity_number = session['identity_number']
    Isexist = USER.query.filter_by(identity_number=identity_number).all()
    print(Isexist)
    if (Isexist):
        if (Isexist[0].transport_number == number):
            flash("您已登记该班次",'info')
            print("您已登记该班次！")
            return redirect(url_for('transport_user.index'))
        if (Isexist[0].transport_number):
            flash("您已登记其他班次！",'info')
            print("您已登记其他班次！")
            return redirect(url_for('transport_user.index'))
    try:
        USER.query.filter_by(identity_number=identity_number).update({'transport_number': number})
        db.session.commit()
        flash('登记成功','success')
        print('登记成功')
    except Exception as e:
        print(e)
        flash("登记出错！",'danger')
        print('登记出错')
        db.session.rollback()
    return redirect(url_for('transport_user.index'))

@transport_user.route('/resultregist/<number>', methods=['GET', 'POST'])
def resultregister(number):
    identity_number = session['identity_number']
    type=session['type']
    start=session['start']
    end=session['end']
    time=session['time']
    q_transport = Transport.query.filter(
        Transport.type.like(type + "%") if type is not None else text(''),
        Transport.start.like(start + "%") if start is not None else text(''),
        Transport.end.like(end + "%") if end is not None else text(''),
        Transport.time.like(time + "%") if time is not None else text('')
    ).all()
    Isexist = USER.query.filter_by(identity_number=identity_number).all()
    print(Isexist)
    if (Isexist):
        if (Isexist[0].transport_number == number):
            flash("您已登记该班次", 'info')
            print("您已登记该班次！")
            return render_template('results.html',transport=q_transport)
        if (Isexist[0].transport_number):
            flash("您已登记其他班次！", 'info')
            print("您已登记其他班次！")
            return render_template('results.html', transport=q_transport)
    try:
        USER.query.filter_by(identity_number=identity_number).update({'transport_number': number})
        db.session.commit()
        flash('登记成功', 'success')
        print('登记成功')
        return render_template('results.html', transport=q_transport)
    except Exception as e:
        print(e)
        flash("登记出错！", 'danger')
        print('登记出错')
        db.session.rollback()
    return render_template('results.html',transport=q_transport)