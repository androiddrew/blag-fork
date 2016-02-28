from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
@app.route('/index')
def index():
    return render_template('blog.html')

if __name__ == "__main__":
    app.run()
