from flask_login import UserMixin, current_user, login_required, login_user,logout_user
from app import db, loginmanager

loginmanager.login_message = "you need to be authenticated in order to access this page".capitalize()
loginmanager.login_message_category = "warning"
loginmanager.login_view = "login"

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250))
    username = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(250))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.firstname} {self.lastname}', '{self.username}', '{self.email}')"

    @loginmanager.user_loader
    def user_loader(id):
        return User.query.get(int(id))


    def __repr__(self):
        return f"User('{self.email}' {self.password})"


    def to_dict(self):
        return {
                "name": self.username,
                "email": self.email,
                "first name": self.firstname
                }



class Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(250), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    nairobi_region = db.Column(db.Integer)
    coastal_region = db.Column(db.Integer)
    western_region = db.Column(db.Integer)
    nothern_region = db.Column(db.Integer)
    name = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '%d'%self.name
    
    def to_dict(self):
        return {
            "id":self.id,
            "name": self.name,
            "category id": self.subcategory_id,
            "nairobi": self.nairobi_region,
            "coast": self.coastal_region,
            "western": self.western_region,
            "nothern": self.nothern_region
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subcategory_id = db.relationship('Subcategory', backref='subcategory', lazy='dynamic')
    description_id = db.relationship('Description', backref='desc', lazy='dynamic')
    name = db.Column(db.String(250))

    def __repr__(self):
        return '%d'%self.name

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description_id = db.relationship('Description', backref='description', lazy='dynamic')
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(250))