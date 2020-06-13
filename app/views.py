from app import app
from app.user import user
from app.admin import admin
from app.framework import login
from app.transportation_models import  Transport,USER
from app.models import Users,Admin
from app import db
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(login, url_prefix='/')

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
user3 = USER(name='王五', email='2983096055@qq.com', address='浙江大学', phone_number='13711111113',
             identity_number='511133200001153024', transport_number='TB128')
db.session.add_all([user1, user2, user3])
db.session.commit()
U1=Users(name='test',pwd='123456',phone='1371111111',idcard='511133200001153018',email='111@qq.com',province='',address='浙江大学',username='Tom')
db.session.add(U1)
db.session.commit()
A1=Admin(name='test',pwd='123456',system=4)
db.session.add(A1)
db.session.commit()
if __name__ == '__main__':
    app.run(debug=True)
