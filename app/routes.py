from app import app
from flask import render_template
from app.forms import LoginForm
@app.route('/')
@app.route('/index')


def index():
   
    return render_template('index.html',title='El título')
@app.route('/search')
def search():
    books={'Title1':['Author1','Description','Summary','Charachters2'],
            'Title3':['Author1','Description','Summary','Charachters2']}
    return render_template('content.html',books=books,title='the search engine')
from flask import render_template, flash, redirect

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

    
