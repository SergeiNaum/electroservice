from decimal import Decimal

from flask import (
    get_flashed_messages, render_template, Blueprint, redirect, url_for, flash, abort

)
from flask_login import current_user

from .forms import ExpenseForm
from .models import Post
from . import db

main = Blueprint('main', __name__)


@main.route('/', endpoint='index')
def index():

    data = {
        'h2_title': 'Расходы',
        'messages': get_flashed_messages(with_categories=True),
        'title': 'РегРЖД - Главная',
        'active_page': 'index',
        'expense_all': Post.query.all()
    }

    return render_template('index.html', data=data)


@main.route('/create', endpoint='create', methods=['post', 'get'])
def create_expense():
    if not current_user.is_authenticated:
        flash('Пользователь не залогинен', 'danger')
        abort(403)

    form = ExpenseForm()

    data = {
        'h2_title': 'создание расхода',
        'messages': get_flashed_messages(with_categories=True),
        'title': 'РегРЖД - создание расхода',
        'active_page': 'index'
    }

    if form.validate_on_submit():
        price = Decimal(form.price.data)
        expense = Post(title=form.title.data, content=form.description.data, price=price, author=current_user)
        db.session.add(expense)
        db.session.commit()

        flash('Запись добавлена', 'success')
        return redirect(url_for('main.index'))

    return render_template('expense_form.html',
                           data=data, form=form)
