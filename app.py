from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from flask_migrate import Migrate
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SECRET_KEY']="merhaba"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

class PostForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField("Email", [validators.DataRequired()])
    submit = SubmitField("Add")
  

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)

db.create_all()

@app.route("/")
def emails():
    contacts = Contact.query.filter_by().all()
    return render_template('index.html', contacts=contacts)

@app.route("/search", methods = ['GET', 'POST'])
def search():
    if request.method == "POST":
        search=request.form["search"]
        contacts=Contact.query.filter_by(name=search).all()
        return render_template('search.html', contacts=contacts)

@app.route("/addemail", methods = ['GET', 'POST'])
def addemail():
    form = PostForm()
    if form.validate_on_submit():        
        entry = Contact(name=form.name.data, email=form.email.data)
        db.session.add(entry)
        db.session.commit()
        contacts = Contact.query.filter_by().all()
        return render_template('index.html', contacts=contacts)
    return render_template("addemail.html", form=form)

if __name__ =="__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=80)