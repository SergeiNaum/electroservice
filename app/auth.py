from flask import (
    Blueprint,
    get_flashed_messages,
    redirect,
    url_for,
    render_template,
    flash,
)
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash

from . import db
from .forms import UserForm, LoginForm
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/reg", methods=["GET", "POST"], endpoint="reg")
def reg():

    form = UserForm()
    data = {
        "h2_title": "Регистрация Нового пользователя",
        "messages": get_flashed_messages(with_categories=True),
        "title": "РегРЖД - Регистрация",
    }

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            flash("Пароли не совподают", "danger")
            return redirect(url_for("auth.reg"))

        existing_user_by_email = User.query.filter_by(email=email).first()
        existing_user_by_username = User.query.filter_by(username=username).first()

        if existing_user_by_email:
            flash("Этот Email уже используется.", "danger")
            return redirect(url_for("auth.reg"))

        if existing_user_by_username:
            flash("Этот login уже занят.", "danger")
            return redirect(url_for("auth.reg"))

        new_user = User(
            email=email, username=username, password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация успешно завершена", "success")
        return redirect(url_for("auth.login"))

    return render_template(
        "authTemplates/registration.html", data=data, form=form, action="Register"
    )


@auth.route("/login", methods=["GET", "post"], endpoint="login")
def login():

    form = LoginForm()

    data = {
        "h2_title": "Вход",
        "messages": get_flashed_messages(with_categories=True),
        "title": "РегРЖД - Вход",
    }

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash("Вход выполнен успешно!", "success")
            login_user(user)
            return redirect(url_for("main.index"))

        flash("Данные введены не корректно. В доступе отказано!", "danger")
        return redirect(url_for("auth.login"))

    return render_template(
        "authTemplates/login.html", data=data, form=form, action="Login"
    )


@auth.route("/logout", endpoint="logout")
def logout():
    logout_user()
    flash("Вы успешно вышли из системы.", "success")
    return redirect(url_for("main.index"))
