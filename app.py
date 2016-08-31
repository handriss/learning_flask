from flask import Flask, render_template, request, redirect, jsonify, g, current_app
import sqlite3
import time


app = Flask(__name__)


@app.route("/")
@app.route("/list")
def index():
    testing_query = query_db("SELECT * FROM story ORDER BY id ASC")
    return render_template('list.html', query=testing_query)


@app.route("/story/<int:story_id>")
@app.route('/modify_user_story/<int:story_id>')
def valami(story_id):
    query = query_db("SELECT * FROM story WHERE id == " + str(story_id) + " ORDER BY id ASC")

    status = ['', '', '', '', '']
    statuses = ['Planning', 'To Do', 'In Progress', 'Review', 'Done']
    status[statuses.index(query[0][-1])] = " selected"
    return render_template('form.html', query=query, status=status, button="Update user story", story_id=story_id)


@app.route('/delete_user_story/<int:story_id>')
def deleting(story_id):
    query_db("DELETE FROM story WHERE id=?", (story_id,))
    testing_query = query_db("SELECT * FROM story ORDER BY id ASC")
    return render_template('list.html', query=testing_query)


@app.route("/story")
def template_test():
    return render_template('form.html', query=['', '', '', '', ''], status='', button="Create user story", story_id="")


@app.route('/save', methods=['POST'])
def saving():
    data = {}
    data["story_title"] = request.form['story_title']
    data["story_content"] = request.form['story_content']
    data["acceptance_criteria"] = request.form['acceptance_criteria']
    data["business_value"] = request.form['business_value']
    data["estimation"] = request.form['estimation']
    data["status"] = request.form['status']

    query = """
        INSERT INTO story (title, content, criteria, business_value, estimation, status)
        VALUES ("{story_title}", "{story_content}", "{acceptance_criteria}", "{business_value}", "{estimation}",
         "{status}")""".format(**data)
    query_db(query)
    return redirect('/')


@app.route('/update/<story_id>', methods=['POST'])
def updating(story_id):

    data = {}
    data["story_title"] = request.form['story_title']
    data["story_content"] = request.form['story_content']
    data["acceptance_criteria"] = request.form['acceptance_criteria']
    data["business_value"] = request.form['business_value']
    data["estimation"] = request.form['estimation']
    data["status"] = request.form['status']

    query_db("UPDATE story SET title=?, content=?, criteria=?, business_value=?, estimation=?, status=? WHERE id=?",
            (request.form['story_title'], request.form['story_content'], request.form['acceptance_criteria'],
    request.form['business_value'],
    request.form['estimation'], request.form['status'], int(request.form['id'])))

    return redirect('/')


DATABASE = 'database.db'


# DB connector
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# Query runner
def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    cur.close()

    # return (rv if rv else None) if one else rv
    return (rv[0] if rv else None) if one else rv


def setup_db():
    query_db("""
    CREATE TABLE IF NOT EXISTS story(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        criteria TEXT,
        business_value INT,
        estimation FLOAT,
        status TEXT
    )
    """)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    with app.app_context():
        setup_db()
        app.run(debug=True)
