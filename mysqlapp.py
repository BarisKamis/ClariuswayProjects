from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from flask_migrate import Migrate
from flask_mysqldb import MySQL
import os

#basedir = os.path.abspath(os.path.dirname(__file__))
#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
#app.config['SECRET_KEY']="merhaba"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)

#migrate = Migrate(app, db)
#with app.app_context():
#    if db.engine.url.drivername == "sqlite":
#        migrate.init_app(app, db, render_as_batch=True)
#    else:
#        migrate.init_app(app, db)


#mycursor = mydb.cursor()
#sql = "DROP TABLE MyUsers"
#mycursor.execute(sql)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE MyUsers ( name VARCHAR(30) NOT NULL,  email VARCHAR(30) NOT NULL)")

class PostForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField("Email", [validators.DataRequired()])
    submit = SubmitField("Add")
  

#class Contact(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(20), nullable=False)
#    email = db.Column(db.String(20), nullable=False)

#db.create_all()

@app.route("/")
def emails():
    #contacts = Contact.query.filter_by().all()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM customers")
    contacts = mycursor.fetchall()
    return render_template('index.html', contacts=contacts)

@app.route("/search", methods = ['GET', 'POST'])
def search():
    if request.method == "POST":
        search=request.form["search"]
        #contacts=Contact.query.filter_by(name=search).all()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM customers ORDER BY" %search
        mycursor.execute(sql)
        contacts = mycursor.fetchall()
        return render_template('search.html', contacts=contacts)

@app.route("/addemail", methods = ['GET', 'POST'])
def addemail():
    form = PostForm()
    if form.validate_on_submit():        
        #entry = Contact(name=form.name.data, email=form.email.data)
        #db.session.add(entry)
        #db.session.commit()
        #contacts = Contact.query.filter_by().all()
        cur = mydb.connection.cursor()
        cur.execute("INSERT INTO MyUsers(name, email) VALUES (%s, %s)", (name, email))
        mydb.connection.commit()
        cur.execute("SELECT * FROM customers")
        contacts = cur.fetchall()
        return render_template('index.html', contacts=contacts)
        #return render_template('index.html', contacts=contacts)
    return render_template("addemail.html", form=form)

if __name__ =="__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=80)