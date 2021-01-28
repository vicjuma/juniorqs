from flask import Flask, jsonify, request, render_template, redirect, url_for, abort, flash
from flask_sqlalchemy import SQLAlchemy
import click
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


app = Flask(__name__, static_url_path='/static')
app.config.from_object('config.Config')

db = SQLAlchemy(app)

loginmanager = LoginManager(app)
loginmanager.login_message = "you need to be authenticated in order to access this page".capitalize()
loginmanager.login_message_category = "warning"
loginmanager.login_view = "login"


"""
 error handling should be done here for the specific error codes
 this includes the forbidden 403, not found 404 and internal server error 
 (should notify the adminstrator and the database be put in a rollback session)
 custom html pages should be used......
"""

@app.cli.command(help="helps in initialising the database")
@click.option("--help", help="you are done")
def create():
    with app.app_context():
        db.create_all()
        click.echo("database created successfully")

def adminsonly():
    def restrict(f):
        @wraps(f)
        def wrapperfunc(*args, **kwargs):
            if current_user.is_authenticated and current_user.is_admin ==False:
                abort(403)
            return f(*args, **kwargs)
        return wrapperfunc
    return restrict


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
        return '%d'%self.id

    @loginmanager.user_loader
    def user_loader(id):
        return User.query.get(int(id))


    def __repr__(self):
        return '<%s>'%self.name


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

#authentication and login

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            password = request.form.get('password')
            data = User(username=username, email=email, firstname=firstname,
            lastname=lastname, password=generate_password_hash(password=password, method='sha256'))
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))
    nxt = request.args.get('next')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user=user, remember=True)
                if nxt:
                    return redirect(nxt)
                flash('you are logged in successfully', 'success')
                return redirect(url_for('dash'))
            flash("wrong password ensure you enter the correct credentials", 'danger')
            return redirect(url_for('login'))
        flash('the user does not exist please create account !', 'danger')
        return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('dash'))
    else:
        return redirect(url_for('dash'))


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    # querry models
    cat = Category.query.all()
    desc = Description.query.all()
    subcategory = Subcategory.query.all()
    return render_template('dashboard.html', cat=cat, desc=desc, subcategory=subcategory)


@app.route('/insert/description', methods=['POST'])
def insert_desc():
    name = request.form.get('itemdescription')
    category_id = request.form.get('category_id')
    subcategory_id = request.form.get('subcategory_id')
    nairobi = request.form.get('nairobi_price')
    coastal = request.form.get('coastal_price')
    nothern = request.form.get('nothern_price')
    western = request.form.get('western_price')
    unit = request.form.get('itemdescriptionunit')

    data = Description(name=name, category_id=category_id,
        subcategory_id=subcategory_id, nairobi_region=nairobi,
        western_region=western, coastal_region=coastal,
        nothern_region=nothern, unit=unit
    )

    db.session.add(data)
    db.session.commit()
    return redirect(url_for('dash'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    return {
            "message": "data updated"
            }

# insert category
@app.route('/add/category', methods=['POST'])
def insert_category():
    data = request.form.get('name')
    cat = Category(name=data)
    db.session.add(cat)
    db.session.commit()
    return redirect(url_for('dash'))

# insert subcategory
@app.route('/add/subcategory', methods=['POST'])
def insert_subcategory():
    data = request.form.get('name')
    category = request.form.get('category')
    cat = Subcategory(name=data, category=category)
    db.session.add(cat)
    db.session.commit()
    return redirect(url_for('dash'))


#delete category
@app.route('/delete/category/', methods=['POST'])
@login_required
@adminsonly()
def delete_category():
    id = request.form.get('id')
    cat = Category.query.filter_by(id=id).first_or_404()
    sub = Subcategory.query.filter_by(category=id).all()
    desc = Description.query.filter_by(category_id=id).all()
    db.session.delete(cat)
    for det in sub:
        db.session.delete(det)
    for det in desc:
        db.session.delete(det)
    db.session.commit()
    return redirect(url_for('dash'))

# delete subcategory
@app.route('/delete/subcategory/', methods=['POST'])
@login_required
@adminsonly()
def delete_subcategory():
    id = request.form.get('id')
    sub = Subcategory.query.filter_by(category=id).first()
    desc = Description.query.filter_by(category_id=id).all()
    db.session.delete(sub)
    for det in desc: db.session.delete(det)
    db.session.commit()
    return redirect(url_for('dash'))

# delete description
@app.route('/delete/description/', methods=['POST'])
@adminsonly()
def delete_description():
    prod_id = request.form.get('id')
    desc = Description.query.filter_by(category_id=prod_id).first()
    db.session.delete(desc)
    db.session.commit()
    return redirect(url_for('dash'))


# updating values in the models
# update category
@app.route('/update/category', methods=['POST'])
def update_category():
    id = request.form.get('id')
    name = request.form.get('id')
    cat = Category.query.filter_by(id=id).first()
    cat.name = name
    db.session.commit()
    return redirect(url_for('dash'))

# update subcategory
@app.route('/update/subcategory', methods=['POST'])
def update_subcategory():
    id = request.form.get('id')
    name = request.form.get('id')
    cat = Subcategory.query.filter_by(id=id).first()
    cat.name = name
    db.session.commit()
    return redirect(url_for('dash'))

# api for data
@app.route('/api', methods=['GET'])
def api_home():
    data = []
    desc = Description.query.all()
    for det in desc:
        data.append(det.to_dict())
    return jsonify(data=data)


if __name__ == '__main__':
    app.run(debug=True)

