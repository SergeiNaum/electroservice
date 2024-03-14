from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo


class UserForm(FlaskForm):
    special_characters = r"!@#$%^&*$$-=_+"

    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"placeholder": "Введите имя пользователя"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Введите Email"})
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=50)],
                             render_kw={"placeholder": "Введите пароль"})
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Введите пароль повторно"})
    submit = SubmitField('Зарегестрировать')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"placeholder": "Введите имя пользователя"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Введите пароль"})
    submit = SubmitField('Войти')


class ExpenseForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()], render_kw={"placeholder": "Введите название расхода"})
    description = TextAreaField('Описание', validators=[DataRequired()], render_kw={"placeholder": "Введите описание расхода"})
    price = DecimalField('Цена', validators=[DataRequired()], render_kw={"placeholder": "Введите цену"})
    submit = SubmitField('Записать')

