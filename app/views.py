from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required

from . import app, db
from .models import News, Category, User
from .forms import NewsForm, RegisterForm, LoginForm

@app.route('/')
def index():
    news_list = News.query.all()
    categories = Category.query.all()
    return render_template('index.html',
                           news=news_list,
                           categories=categories)

@app.route('/news_detail/<int:id>')
def news_detail(id):
    news = News.query.get(id)
    categories = Category.query.all()
    return render_template('news_detail.html',
                           news=news,
                           categories=categories)

@app.route('/category/<int:id>')
def news_in_category(id):
    category = Category.query.get(id)
    news = category.news
    category_name = category.titleН
    categories = Category.query.all()
    return render_template('category.html',
                           news=news,
                           category_name=category_name,
                           categories=categories)

@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        news = News()
        news.title = form.title.data
        news.text = form.text.data
        news.category_id = form.category.data
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('news_detail', id=news.id))
    return render_template('add_news.html',
                           form=form,
                           categories=categories)

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.username = form.username.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        return render_template('login.html', form=form, error='Неверное имя пользователя или пароль')
    return render_template('login.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))