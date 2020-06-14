from flask import render_template, url_for,session,Blueprint,flash
from flask import request, redirect
from app import db
from sqlalchemy import func
from app.models import Popflow,Comment,Information,DecimalEncoder
import json


population_user=Blueprint('population_user',__name__)

@population_user.before_request
def before_user():
    if 'identity' in session and session['identity']==5:
        return redirect(url_for('population_admin.index'))
    else:
        pass

@population_user.route("index.html")
def index():
    result = Popflow.query.with_entities(
                Popflow.people_province,
                func.sum(Popflow.people_inflow).label('sum_inflow'),
                func.sum(Popflow.people_outflow).label('sum_outflow')
                ).group_by(Popflow.people_province).all()
    if result:
        Data = []
        Gdata = []
        for i in result:
            tu = {
                "province": i.people_province,
                "inflow": i.sum_inflow,
                "outflow": i.sum_outflow
            }
            tf={
                "name":i.people_province,
                "value":i.sum_inflow
            }
            Data.append(tu)
            Gdata.append(tf)
        Gdata = json.dumps(Gdata,cls=DecimalEncoder)
        test1={"name":"浙江", "value":99999}
        test1=json.dumps(test1,ensure_ascii=False)
        test1 = json.dumps(test1,cls=DecimalEncoder)
        test='上海'
        return render_template('popu_user_index.html',data = Data,Gdata=Gdata,test=test,test1=test1)
    return render_template('popu_user_index.html')

@population_user.route("/details-1/<province>",methods=['GET','POST'])
def details_1(province):
    if not province:
        province = '浙江'
        return render_template('details-1.html', cur_province = province)

    result = Information.query.filter(Information.info_type == 0, Information.info_province == province).all()
    if result:
        Data = []
        for i in result:
            tu = {
                "ID": i.info_ID,
                "title": i.info_title,
                "text": i.info_text,
                "time": i.info_time
            }
            Data.append(tu)
        return render_template('details-1.html', data = Data, cur_province = province)
    return render_template('details-1.html', cur_province = province)


@population_user.route("/details-2/<province>")
def details_2(province):
    if not province:
        province = '浙江'
        return render_template('details-2.html', cur_province = province)

    result = Information.query.filter(Information.info_type == 1, Information.info_province == province).all()
    if result:
        Data = []
        for i in result:
            tu = {
                "ID": i.info_ID,
                "title": i.info_title,
                "text": i.info_text,
                "time": i.info_time
            }
            Data.append(tu)
        return render_template('details-2.html', data = Data, cur_province = province)
    return render_template('details-2.html', cur_province = province)

@population_user.route("/details-3/<province>")
def details_3(province):
    if not province:
        province = '浙江'
        return render_template('details-3.html', cur_province = province)

    result = Information.query.filter(Information.info_type == 2, Information.info_province == province).all()
    if result:
        Data = []
        for i in result:
            tu = {
                "ID": i.info_ID,
                "title": i.info_title,
                "text": i.info_text,
                "time": i.info_time
            }
            Data.append(tu)
        return render_template('details-3.html', data = Data, cur_province = province)
    return render_template('details-3.html', cur_province = province)

@population_user.route("/details-4/<province>")
def details_4(province):
    if not province:
        province = '浙江'
        return render_template('details-4.html', cur_province = province)

    result = Information.query.filter(Information.info_type == 3, Information.info_province == province).all()
    if result:
        Data = []
        for i in result:
            tu = {
                "ID": i.info_ID,
                "title": i.info_title,
                "text": i.info_text,
                "time": i.info_time
            }
            Data.append(tu)
        return render_template('details-4.html', data = Data, cur_province = province)
    return render_template('details-4.html', cur_province = province)

@population_user.route("/get-page-details/<iid>", methods=['GET'])
def get_page_details(iid):
    result = Information.query.get(iid)
    if result:
        comt_result = Comment.query.filter(Comment.info_ID == iid).all()
        if comt_result:
            Data = []
            for i in comt_result:
                tu = {
                    "comt_user_ID":i.user_name,
                    "comt_time":i.comment_time,
                    "comt_text":i.comment_text
                }
                Data.append(tu)
            return render_template('page-details.html', data = Data,info_ID = result.info_ID, info_title = result.info_title, info_text = result.info_text)
        return render_template('page-details.html', info_ID = result.info_ID, info_title = result.info_title, info_text = result.info_text)
    return render_template('page-details.html')

@population_user.route('/addComt', methods=['POST'])
def addComt():
    if 'name' not in session:
        flash('请先登录！','warning')
        return redirect(url_for('.index'))
    text = request.form.get("comt_text")
    iid = request.form.get("info_ID")
    if not text:
        flash("输入参数错误：评论为空",'warning')
    record = Comment(user_name=session.get('name'),comment_text = text, info_ID = iid)
    db.session.add(record)
    db.session.commit()
    return redirect(url_for('.get_page_details', iid = iid))

@population_user.route("/switch_province1", methods=['POST'])
def switch_province1():
    province = request.form.get("choose")
    if not province:
        province = '浙江'
    return redirect(url_for('.details_1', province=province))

@population_user.route("/switch_province2", methods=['POST'])
def switch_province2():
    province = request.form.get("choose")
    if not province:
        province = '浙江'
    return redirect(url_for('.details_2', province=province))

@population_user.route("/switch_province3", methods=['POST'])
def switch_province3():
    province = request.form.get("choose")
    if not province:
        province = '浙江'
    return redirect(url_for('.details_3', province=province))

@population_user.route("/switch_province4", methods=['POST'])
def switch_province4():
    province = request.form.get("choose")
    if not province:
        province = '浙江'
    return redirect(url_for('.details_4', province=province))