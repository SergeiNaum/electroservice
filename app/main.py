from flask import (
    Flask, get_flashed_messages, render_template,

)


from app.app_config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)









if __name__ == "__main__":
    app