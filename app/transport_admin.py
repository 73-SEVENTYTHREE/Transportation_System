from flask import render_template, request, flash, make_response, url_for, redirect,Blueprint,session
from app import db
from app.transportation_models import  Transport
from io import BytesIO
import xlsxwriter
from flask_mail import Mail, Message
from sqlalchemy import text
from app import mail

def create_flie(users):
    output=BytesIO()
    workbook=xlsxwriter.Workbook(output,{'in_memory':True})
    worksheet=workbook.add_worksheet('download')
    title = ["姓名", "邮箱", "手机号码", "身份证号码", "地址", "乘车班次",'乘车日期']
    worksheet.write_row('A1', title)
    for i in range(len(users)):
        row = [users[i].name, users[i].email, users[i].phone_number, users[i].identity_number, users[i].address,
               users[i].transport_number,users[i].transport.time.strftime('%Y-%m-%d')]
        print(row)
        print(users[i].transport.time)
        worksheet.write_row('A' + str(i + 2), row)
    workbook.close()
    response = make_response(output.getvalue())
    output.close()
    return response



transport_admin = Blueprint('transport_admin', __name__)

@transport_admin.before_request
def before_admin():
    if 'identity' in session and session['identity']==4:
        pass
    else:
        flash('小火汁，你的思想很危险！','danger')
        return redirect(url_for('transport_user.index'))

@transport_admin.route('/', methods=['GET','POST'])
def index():
    transport1 = Transport.query.filter_by(type=1).all()
    transport0 = Transport.query.filter_by(type=0).all()
    print(transport1)
    return render_template('manager_index.html', transport0=transport0, transport1=transport1)

@transport_admin.route('/manager_email', methods=['GET', 'POST'])
def sendemail():
    if request.method == 'POST':
        choice=request.form['choice']
        if(choice=='0'):
            return render_template('manager_email.html')
        number = request.form["number"]
        if(number==''):
            flash('请输入班次编号！','warning')
            redirect(url_for('sendemail'))
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
                    flash('发送成功','success')
                except Exception as e:
                    print(e)
                    flash('发送失败', 'danger')
    return render_template("manager_email.html")

@transport_admin.route('/manager_export',methods=['GET','POST'])
def exportuser():
    if request.method=='POST':
        number = request.form["number"]
        time = request.form["time"]
        if (number == "" and time == ""):
            flash("请输入导出条件！",'warning')
            print("请输入导出条件")
            return render_template('manager_export.html')
        targets = Transport.query.filter(
            Transport.number.like(number+"%") if number is not None else text(""),
            Transport.time.like(time+"%") if time is not None else text("")
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
                flash("该班次无乘客登记！",'warning')
                print('该班次无乘客登记！')
        else:
            flash("无班次信息！",'warning')
            print("无班次信息！")
    return render_template("manager_export.html")


@transport_admin.route('/manager_issue',methods=['GET','POST'])
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
            flash("数据库内已有该日期该班次信息！",'warning')
        else:
            try:
                new_transport = Transport(number=number, type=type, start=start, end=end, time=time)
                db.session.add(new_transport)
                db.session.commit()
                flash('添加成功','success')
            except Exception as e:
                print(e)
                flash("添加出错！",'danger')
                db.session.rollback()
    return render_template("manager_issue.html")

