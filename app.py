import importlib
import sys
from datetime import timedelta
from io import BytesIO

import xlsxwriter
from flask import Flask, render_template, request, flash, make_response, url_for, session, redirect
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

import email_config

importlib.reload(sys)
app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql://root:2569535507Lw@127.0.0.1/COVID"  # 自己的数据库配置，先预先在mysql中创建COVID数据库 格式：mysql://账号:密码@127.0.0.1/COVID
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(email_config)
app.secret_key = 'DAFSDFDAFSDJGJ'
db = SQLAlchemy(app)
mail = Mail()
mail.init_app(app)


class USER(db.Model):
    __tablename__ = "users"
    identity_number = db.Column(db.String(30), primary_key=True)
    email=db.Column(db.String(30))
    address = db.Column(db.String(30))
    name = db.Column(db.String(20))
    phone_number = db.Column(db.String(11),unique=True)
    transport_number=db.Column(db.String(10),db.ForeignKey('transport.number'))
    transport=db.relationship('Transport',backref='User')



class Transport(db.Model):
    __tablename__='transport'
    number=db.Column(db.String(10),primary_key=True)
    type=db.Column(db.Integer)
    start=db.Column(db.String(10))
    end=db.Column(db.String(10))
    time=db.Column(db.Date)

def create_flie(users):
    output=BytesIO()
    workbook=xlsxwriter.Workbook(output,{'in_memory':True})
    worksheet=workbook.add_worksheet('download')
    title = ["姓名", "邮箱", "手机号码", "身份证号码", "乘车班次", "地址"]
    worksheet.write_row('A1', title)
    for i in range(len(users)):
        row = [users[i].name, users[i].email, users[i].phone_number, users[i].identity_number,
               users[i].transport_number, users[i].address]
        worksheet.write_row('A' + str(i + 2), row)
    workbook.close()
    response = make_response(output.getvalue())
    output.close()
    return response


@app.route('/clear')
def clear():
    session.clear()
    return redirect(url_for('index'))


@app.route("/", methods=['GET', 'POST'])
def index():
    print(session.get('identity_number'))
    name = session.get('name')
    if (name is None):
        name = ""
    transport = Transport.query.all()
    return render_template('transportation.html', transport=transport, name=name)


@app.route('/search', methods=['GET', 'POST'])
def turnsearch():
    if 'identity_number' in session:
        return render_template('search.html')
    else:
        flash('您还未注册个人信息！')
        transport = Transport.query.all()
        return render_template('transportation.html', transport=transport)


@app.route('/results', methods=['GET', 'POST'])
def turnresult():
    return render_template('results.html')


@app.route('/msg_input', methods=['GET', 'POST'])
def turninput():
    return render_template('msg_input.html')


@app.route('/indexregister/<number>', methods=['GET', 'POST'])
def indexregister(number):
    session['transport_number'] = number
    if 'identity_number' in session:
        return redirect(url_for('searchregister', number=session['transport_number']))
    return render_template('msg_input.html')


@app.route('/register', methods=['GET', 'POST'])
def msg_input():
    if request.method == 'POST':
        if 'transport_number' in session:
            name = request.form['name']
            identity_number = request.form['identity_number']
            address = request.form['address']
            phone_number = request.form['phone_number']
            email = request.form['email']
            session['identity_number'] = identity_number
            session['name'] = name
            session['address'] = address
            session['phone_number'] = phone_number
            session['email'] = email
            q_user = USER.query.filter_by(identity_number=identity_number).first()
            if (q_user):
                flash('您已填写信息！')
                print('您已填写信息！')
                return redirect(url_for('turnsearch'))
            else:
                try:
                    new_user = USER(name=name, identity_number=identity_number, email=email, address=address,
                                    phone_number=phone_number)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('填写成功！')
                    print('添加成功')
                    return render_template('search.html')
                except Exception as e:
                    print(e)
                    flash('添加出错')
                    db.session.rollback()
        else:
            name = request.form['name']
            identity_number = request.form['identity_number']
            address = request.form['address']
            phone_number = request.form['phone_number']
            email = request.form['email']
            session['identity_number'] = identity_number
            session['name'] = name
            session['address'] = address
            session['phone_number'] = phone_number
            session['email'] = email
            q_user = USER.query.filter_by(identity_number=identity_number).first()
            if (q_user):
                if (q_user.transport_number):
                    flash('您已登记！')
                    return render_template('msg_input.html')
            else:
                try:
                    new_user = USER(name=name, identity_number=identity_number, email=email, address=address,
                                    phone_number=phone_number, transport_number=session['transport_number'])
                    db.session.add(new_user)
                    db.session.commit()
                    flash('登记成功！')
                    return render_template('search.html')
                except Exception as e:
                    print(e)
                    flash('添加出错')
                    db.session.rollback()
    return render_template('msg_input.html')


@app.route('/searchtransport', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        type = request.form['type']
        start = request.form['start']
        end = request.form['end']
        time = request.form['time']
        if (type == "" and start == "" and end == "" and time == ""):
            flash("请输入查询条件！")
            print("请输入查询条件！")
            return redirect(url_for('turnsearch'))
        q_transport = Transport.query.filter(
            Transport.type.like(type) if type is not "" else "",
            Transport.start.like(start) if start is not "" else "",
            Transport.end.like(end) if end is not "" else "",
            Transport.time.like(time) if time is not "" else ""
        ).all()
        if (q_transport):
            session['search_time'] = 1
            return render_template('results.html', transport=q_transport)
        else:
            flash('数据库中无该条件班次！')
            return redirect(url_for('index'))


@app.route('/searchregist/<number>', methods=['GET', 'POST'])
def searchregister(number):
    identity_number = session['identity_number']
    Isexist = USER.query.filter_by(identity_number=identity_number).all()
    print(Isexist)
    if (Isexist):
        if (Isexist[0].transport_number == number):
            flash("您已登记该班次")
            print("您已登记该班次！")
            return redirect(url_for('index'))
        if (Isexist[0].transport_number):
            flash("您已登记其他班次！")
            print("您已登记其他班次！")
            return redirect(url_for('index'))
    try:
        USER.query.filter_by(identity_number=identity_number).update({'transport_number': number})
        db.session.commit()
        flash('登记成功')
        print('登记成功')
    except Exception as e:
        print(e)
        flash("登记出错！")
        print('登记出错')
        db.session.rollback()
    return redirect(url_for('index'))


@app.route('/manager_email', methods=['GET', 'POST'])
def sendemail():
    if request.method == 'POST':
        number = request.form["number"]
        content = request.form["content"]
        q_number = Transport.query.filter_by(number=number).all()
        if (q_number):
            if (q_number[0].User):
                emails = []
                for i in q_number[0].User:
                    emails.append(i.email)
                message=Message(subject="居家隔离提醒",recipients=emails,body=content)
                try:
                    mail.send(message)
                    return "发送成功！"
                except Exception as e:
                    print(e)
                    return "发送失败！"
    return render_template("manager_email.html")

@app.route('/manager_export',methods=['GET','POST'])
def exportuser():
    if request.method=='POST':
        number = request.form["number"]
        time = request.form["time"]
        if (number == "" and time == ""):
            flash("请输入导出条件！")
            print("请输出导出条件")
            return render_template('manager_export.html')
        targets = Transport.query.filter(
            Transport.number.like(number) if number is not "" else "",
            Transport.time.like(time) if time is not "" else ""
        ).all()
        print(targets)
        if (len(targets) != 0):
            if (len(targets[0].User) != 0):
                muser = []
                for target in targets:
                    for tuser in target.User:
                        print(tuser)
                        muser.append(tuser)
                        print(muser)
                response = create_flie(muser)
                response.headers['Content-Type'] = 'utf=8'
                response.headers['Cache-Control'] = 'no-cache'
                response.headers['Content-Disposition'] = 'attachment;filename=download.xlsx'
                return response
            else:
                flash("该班次无乘客登记！")
                print('该班次无乘客登记！')
        else:
            flash("无班次信息！")
            print("无班次信息！")
    return render_template("manager_export.html")


@app.route('/manager_issue',methods=['GET','POST'])
def issue():
    if request.method == 'POST':
        number = request.form["number"]
        type = request.form["flightOrTrain"]
        if (type == "flight"):
            type = 1
        else:
            type = 0
        start = request.form["start"]
        end = request.form["end"]
        time = request.form["time"]
        q_number=Transport.query.filter_by(number=number,time=time).first()
        if(q_number):
            flash("数据库内已有该日期该班次信息！")
        else:
            try:
                new_transport = Transport(number=number, type=type, start=start, end=end, time=time)
                db.session.add(new_transport)
                db.session.commit()
            except Exception as e:
                print(e)
                flash("添加出错！")
                db.session.rollback()
    return render_template("manager_issue.html")


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    transport1 = Transport.query.filter_by(type=1).all()
    transport0 = Transport.query.filter_by(type=0).all()
    return render_template('manager_index.html', transport0=transport0, transport1=transport1)


db.drop_all()
db.create_all()
plane1 = Transport(number='TB127', type='1', start='杭州', end='成都', time='2020-06-06')
plane2 = Transport(number='TB128', type='1', start='杭州', end='成都', time='2020-06-06')
plane3 = Transport(number='TB129', type='1', start='杭州', end='成都', time='2020-06-06')
plane4 = Transport(number='TB110', type='0', start='杭州', end='成都', time='2020-06-08')
db.session.add_all([plane1, plane2, plane3, plane4])
db.session.commit()
user1 = USER(name='张三', email='2569535507@qq.com', address='浙江大学', phone_number='13711111111',
             identity_number='511133200001153022', transport_number='TB127')
user2 = USER(name='李四', email='15944065615@163.com', address='浙江大学', phone_number='13711111112',
             identity_number='511133200001153023', transport_number='TB127')
user3 = USER(name='王五', email='15944065615@163.com', address='浙江大学', phone_number='13711111113',
             identity_number='511133200001153024', transport_number='TB128')
db.session.add_all([user1, user2, user3])
db.session.commit()
if __name__ == '__main__':
    app.run(debug=True)
