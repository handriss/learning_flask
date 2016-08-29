from flask import Flask, render_template, request, redirect
app = Flask(__name__)


@app.route("/")
def index():
    return "it works"


@app.route("/story")
def template_test():
    return render_template('form.html')


@app.route('/save', methods=['POST'])
def signup():
    story_title = request.form['story_title']
    print("The story title is '" + story_title + "'")
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
