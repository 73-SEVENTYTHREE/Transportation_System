from app import db

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

