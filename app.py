from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.fields.html5 import EmailField

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

fname = ""
lname = ""
org = ""
email = ""
phone = ""
product = ""
review = ""

class ReviewForm(Form):
	fname = TextField('First Name *', validators=[validators.DataRequired()])
	lname = TextField('Last Name *', validators=[validators.DataRequired()])
	org = TextField('Name Of Organisation/Institution *', validators=[validators.DataRequired()])
	email = EmailField('Email ID *', validators=[validators.DataRequired(), validators.Email("Please enter an email address")])
	phone = TextField('Phone Number *', validators=[validators.DataRequired(), validators.Length(min=10, max=10, message="Phone number should be of 10 digits")])
	product = TextField('Which product are you reviewing? *', validators=[validators.DataRequired()])
	review = TextField('What\'s your review? *', validators=[validators.DataRequired(), validators.Length(min=20, max=100, message=u'Review must be of atleast 20 characters and a maximum of 100 characters')])

@app.route("/", methods=['GET', 'POST'])
def index():
	form = ReviewForm(request.form)
	if(request.method == 'POST'):
		if(form.validate()):
			global fname, lname, email, phone, org, product, review
			fname = request.form['fname']
			lname = request.form['lname']
			org = request.form['org']
			email = request.form['email']
			phone = request.form['phone']
			product = request.form['product']
			review = request.form['review']
			f = open("reviews.txt", "a+")
			f.write(fname + "," + lname + "," + org + "," + email + "," + phone + "," + product + "," + review + '\n')
			return render_template('submission.html', fname=fname, lname=lname, org=org, email=email, phone=phone, product=product, review=review)
	return render_template('index.html', form=form)

@app.route("/review-submitted")
def thanks():
	return render_template("thanks.html")

@app.route("/display", methods=['GET','POST'])
def display():
	review_list = []
	with open("reviews.txt") as f:
		lines = f.readlines()
		for line in lines:
			review_list += [line.split(",")]
	return render_template('display.html', review_list = review_list)

@app.errorhandler(404)
def not_found(e):
	return render_template("404.html")

@app.errorhandler(500)
def application_error(e):
	return 'Sorry, unexpected error: {}'.format(e), 500

if(__name__ == "__main__"):
	app.run(host="localhost",port="9999")
