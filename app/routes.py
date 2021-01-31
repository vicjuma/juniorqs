from app.models import User, Category, Description, Subcategory
from flask import Flask, jsonify, request, render_template, redirect, url_for, abort, flash
import click
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app.forms import RegistrationForm, LoginForm
from app import app, db, bcrypt


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

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash(f'Account created successfully, log in', 'success')
                return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    nxt = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('the user does not exist please create account !', 'danger')
                return redirect(url_for('register'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


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
    return redirect(url_for('home'))

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
    return redirect(url_for('home'))

# insert subcategory
@app.route('/add/subcategory', methods=['POST'])
def insert_subcategory():
    data = request.form.get('name')
    category = request.form.get('category_id')
    cat = Subcategory(name=data, category=category)
    db.session.add(cat)
    db.session.commit()
    return redirect(url_for('home'))


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
    return redirect(url_for('home'))

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
    return redirect(url_for('home'))

# delete description
@app.route('/delete/description/<int:id>', methods=['POST'])
@adminsonly()
def delete_description(id):
    desc = Description.query.filter_by(category_id=id).first()
    db.session.delete(desc)
    db.session.commit()
    flash('description sucessfully deleted', 'danger')
    return redirect(url_for('home'))


# updating values in the models
# update category
@app.route('/update/category', methods=['POST'])
def update_category():
    id = request.form.get('id')
    name = request.form.get('id')
    cat = Category.query.filter_by(id=id).first()
    cat.name = name
    db.session.commit()
    return redirect(url_for('home'))

# update subcategory
@app.route('/update/subcategory', methods=['POST'])
def update_subcategory():
    id = request.form.get('id')
    name = request.form.get('id')
    cat = Subcategory.query.filter_by(id=id).first()
    cat.name = name
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/description/<int:id>', methods=['GET', 'POST'])
@adminsonly()
def update_description(id):
    desc = Description.query.filter_by(id=id).first_or_404()
    if request.method == 'GET':
        return render_template('update.html', desc=desc)
    desc.name = request.form.get('name')
    desc.unit = request.form.get('unit')
    desc.western_region = int(request.form.get('western_price'))
    desc.nairobi_region = int(request.form.get('nairobi_price'))
    desc.nothern_region = int(request.form.get('nothern_price'))
    desc.coastal_region = int(request.form.get('coastal_price'))
    db.session.commit()
    return redirect(url_for('home'))

# api for data
@app.route('/api', methods=['GET'])
def api_home():
    data = []
    desc = Description.query.all()
    for det in desc:
        data.append(det.to_dict())
    return jsonify(data=data)
