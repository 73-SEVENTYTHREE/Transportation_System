from flask import Flask, render_template, url_for,jsonify,flash,session,Blueprint
from flask import request,redirect
from app import db
from app.models import Users, Admin,Information,Comment,Popflow
listInfoType = [
    'IndustryRestart','Quarantine','Transportation','MedicalService'
]

listInfoProvince = [
    'Guangdong', 'Zhejiang'
]


population_admin=Blueprint('population_admin',__name__)

@population_admin.before_request
def before_admin():
    if 'identity' in session and session['identity']==5:
        pass
    else:
        flash('小火汁，你的思想很危险！','danger')
        return redirect(url_for('population_user.index'))

@population_admin.route('/',methods=['GET'])
def index():
    return render_template('home.html', title='admin', type=listInfoType)

@population_admin.route('/population.html',methods=['GET'])
def population():
    return render_template('population.html', title='admin', type=listInfoType)


@population_admin.route('/information.html',methods=['GET'])
def information():
    return render_template('information.html', title='admin', type=listInfoType)


@population_admin.route('/comments.html',methods=['GET'])
def comments():
    return render_template('comments.html', title='admin', type=listInfoType)


@population_admin.route('/comments_delete.html',methods=['GET'])
def comments_delete():
    return render_template('comments_delete.html', title='admin', type=listInfoType)


# 查询并返回符合类型的所有讯息
@population_admin.route('/information_check/<int:itype>', methods=['GET'])
def information_check(itype):
    if (itype < 0 or itype >= 4):
        return "输入参数有误：没有传入有效信息类型"

    result = Information.query.filter(Information.info_type == itype).all()
    if result:
        Data = []
        for i in result:
            tu = {
                "info_ID": i.info_ID,
                "info_title": i.info_title,
                "info_time": i.info_time
            }
            Data.append(tu)
        return render_template('information_delete.html', title='admin', data=Data)

    return render_template('information_delete.html', title='admin')


# 删除一条讯息
@population_admin.route('/delInfo/<iid>', methods=['GET'])
def delInfo(iid):
    itype = 0
    URL = url_for('.information_check', itype = itype)

    result = Information.query.get(iid)
    if result:
        comts = Comment.query.filter(Comment.info_ID == iid)
        if comts:
            for i in comts:
                db.session.delete(i)
            db.session.commit()
        itype = result.info_type
        URL = url_for('.information_check', itype = itype)
        db.session.delete(result)
        db.session.commit()
        
        return render_template('notice.html', notice='删除成功'\
            , URL=URL)
    
    return render_template('notice.html', notice='删除失败'\
        , URL=URL)


# 添加一条讯息
@population_admin.route('/addInfo', methods=['POST'])
def addInfo():
    itype = request.form.get("info_type")
    title = request.form.get("info_title")
    text = request.form.get("info_text")
    time = request.form.get("info_time")

    URL = url_for('.information')
    if not all([title,text]):    
        return render_template('notice.html', notice='输入参数有误：标题或内容为空', URL=URL)
    if itype not in listInfoType:
        return render_template('notice.html', notice='输入参数有误：没有传入有效信息类型', URL=URL)
    #要记得补全一些未填充的：省份
    record = Information(info_type = listInfoType.index(itype), info_province=session.get('province'), info_title = title, info_text = text, info_time = time)
    db.session.add(record)
    db.session.commit()
    return render_template('notice.html', notice='插入成功', URL=URL)


# 更新一条人口流动信息
@population_admin.route('/addPopInfo', methods=['POST'])
def addPopInfo():
    infl = request.form.get("people_inflow")
    oufl = request.form.get("people_outflow")
    
    URL = 'population.html'

    if not all([infl,oufl]):
        return render_template('notice.html', notice='更新失败'\
            , URL=URL)
    #要记得补全一些未填充的：省份
    record = Popflow(people_province=session.get('province'), people_inflow = int(infl), people_outflow = int(oufl))
    db.session.add(record)
    db.session.commit()
    return render_template('notice.html', notice='更新成功'\
            , URL=URL)


# 查询并返回符合类型的所有讯息
@population_admin.route('/comt_information_check/<int:itype>', methods=['GET'])
def comt_information_check(itype):
    if (itype < 0 or itype >= 4):
        flash("输入参数有误：没有传入有效信息类型")
    result = Information.query.filter(Information.info_type == itype).all()
    if result:
        Data = []
        for i in result:
            tu = {
                "info_ID": i.info_ID,
                "info_title": i.info_title,
                "info_time": i.info_time
            }
            Data.append(tu)
        return render_template('comments.html', title='admin', data=Data)

    return render_template('comments.html', title='admin')


# 查询并返回某条讯息下的所有评论
@population_admin.route('/comment_check/<iid>', methods=['GET'])
def comment__check(iid):
    result = Comment.query.filter(Comment.info_ID == iid).all()
    if result:
        Data = []
        for i in result:
            tu = {
                "info_ID": i.info_ID,
                "comt_ID": i.comment_ID,
                "user_ID": i.user_ID,
                "comt_text": i.comment_text,
                "comt_time": i.comment_time
            }
            Data.append(tu)
        # return Data[0]['comt_ID']
        return render_template('comments_delete.html', title='admin', data=Data)

    return render_template('comments_delete.html', title='admin')


#删除某一条评论
@population_admin.route('/delComt/<cid><sep><iid>', methods=['GET'])
def delComt(cid, sep, iid):
    cid1 = cid.split("|")[0]
    iid = cid.split("|")[1]
    result = Comment.query.get(cid1)
    URL = url_for('.comment__check', iid = iid)
    if result:
        db.session.delete(result)
        db.session.commit()
        return render_template('notice.html', notice='删除成功'\
            , URL=URL)
    
    return render_template('notice.html', notice='删除失败'\
        , URL=URL)