from flask import request, render_template, flash, url_for, redirect, g,session


from app import app

@app.route('/')
def index():
	return render_template('index.html')


