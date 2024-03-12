from flask import (
    Flask, get_flashed_messages, render_template,

)


from app.app_config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)

    return render_template('index.html', title='РегРЖД - Главная', messages=messages)


@app.route('/reg')
def reg():
    messages = get_flashed_messages(with_categories=True)

    return render_template('authTemplates/registration.html', title='РегРЖД - Регистрация', messages=messages)



@app.route('/login')
def login():
    messages = get_flashed_messages(with_categories=True)

    return render_template('authTemplates/login.html', title='РегРЖД - Вход', messages=messages)


@app.route('/logout')
def logout():
    messages = get_flashed_messages(with_categories=True)

    return render_template('authTemplates/login.html', title='РегРЖД-Вход', messages=messages)



if __name__ == "__main__":
    app.run(debug=True)
