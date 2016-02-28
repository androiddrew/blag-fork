from flask import Flask, render_template

from config import config_by_name

app = Flask(__name__)
app.config.from_object(config_by_name['dev'])


@app.route("/")
@app.route('/index')
def index():
    return render_template('blog.html')

if __name__ == "__main__":
    app.run()
