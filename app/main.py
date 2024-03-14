from decimal import Decimal

from flask import (
    get_flashed_messages,
    render_template,
    Blueprint,
    redirect,
    url_for,
    flash,
    abort,
    request,
)
from flask_login import current_user

from .forms import ExpenseForm
from .models import Post
from . import db

main = Blueprint("main", __name__)


@main.route("/", endpoint="index")
def index():

    user = current_user
    data = {
        "h2_title": "Расходы",
        "messages": get_flashed_messages(with_categories=True),
        "title": "РегРЖД - Главная",
        "active_page": "index",
        # 'expense_all': Post.query.all()
        "expense_all": user.posts if user.is_authenticated else None,
    }

    return render_template("index.html", data=data)


@main.route("/create", endpoint="create", methods=["post", "get"])
def create_expense():
    if not current_user.is_authenticated:
        flash("Пользователь не залогинен", "danger")
        abort(403)

    form = ExpenseForm()

    data = {
        "h2_title": "создание расхода",
        "messages": get_flashed_messages(with_categories=True),
        "title": "РегРЖД - создание расхода",
    }

    if form.validate_on_submit():
        price = Decimal(form.price.data)
        expense = Post(
            title=form.title.data,
            content=form.description.data,
            price=price,
            author=current_user,
        )
        db.session.add(expense)
        db.session.commit()

        flash("Запись добавлена", "success")
        return redirect(url_for("main.index"))

    return render_template("expense_form.html", data=data, form=form)


@main.route(
    "/expense/<int:expense_id>", endpoint="expense_detail", methods=["post", "get"]
)
def expense_detail(expense_id: int):

    form = ""
    expense = ""

    if not current_user.is_authenticated:
        flash("Пользователь не залогинен", "danger")
        abort(403)

    data = {
        "h2_title": "Редактировать",
        "messages": get_flashed_messages(with_categories=True),
        "title": "РегРЖД - Редактировать запись трат",
    }

    user = current_user
    if user:
        expense = Post.query.filter_by(id=expense_id, author=user).first()

        if expense is None:
            flash("Запись не найдена или у вас нет прав на редактирование", "danger")
            return redirect(url_for("main.index"))

        form = ExpenseForm(obj=expense)

        if form.validate_on_submit():
            expense.title = form.title.data if form.title.data else expense.title
            expense.content = (
                form.description.data if form.description.data else expense.content
            )
            expense.price = (
                Decimal(form.price.data) if form.price.data else expense.price
            )
            db.session.commit()

            flash("Запись успешно отредактирована", "success")
            return redirect(url_for("main.index"))

    return render_template(
        "expense_form.html",
        expense_id=expense_id,
        data=data,
        form=form,
        expense=expense,
    )


@main.route(
    "/expense/delete/<int:expense_id>", endpoint="delete", methods=["post", "get"]
)
def expense_delete(expense_id: int):
    form = ""
    expense = ""

    if not current_user.is_authenticated:
        flash("Пользователь не залогинен", "danger")
        abort(403)

    data = {
        "h2_title": "Удалить",
        "messages": get_flashed_messages(with_categories=True),
        "title": "РегРЖД - Удаление записи расходов",
    }

    user = current_user

    if user:
        expense = Post.query.filter_by(id=expense_id, author=user).first()

        if expense is None:
            flash("Запись не найдена или у вас нет прав на удаление", "danger")
            return redirect(url_for("main.index"))

        if request.method == "POST":
            if request.form.get("confirm") == "Да!":
                db.session.delete(expense)
                db.session.commit()
                flash("Запись успешно удалена", "success")
                return redirect(url_for("main.index"))
            else:
                flash("Удаление отменено", "info")
                return redirect(url_for("main.index"))

        return render_template("del.html", data=data, form=form, expense=expense)
