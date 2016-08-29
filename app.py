from flask import Flask, render_template, request, redirect, jsonify, g, current_app
import sqlite3
import time


app = Flask(__name__)


@app.route("/")
def index():
    return "it works"

    for query in query_db('SELECT * FROM story'):
        print(query)

@app.route("/story")
def template_test():
    return render_template('form.html')


@app.route('/save', methods=['POST'])
def signup():
    data = {}
    data["story_title"] = request.form['story_title']
    data["story_content"] = request.form['story_content']
    data["acceptance_criteria"] = request.form['acceptance_criteria']
    data["business_value"] = request.form['business_value']
    data["estimation"] = request.form['estimation']
    data["status"] = request.form['status']

    print(data)

    query = """
        INSERT INTO story (title, content, criteria, business_value, estimation, status)
        VALUES ("{story_title}", "{story_content}", "{acceptance_criteria}", "{business_value}", "{estimation}",
        , "{status}")""".format(**data)
    return redirect('/')

# tweet = request.get_json()
#     tweet["poster"] = prevent_injection(tweet["poster"][:20].strip())       # validation
#     tweet["content"] = prevent_injection(tweet["content"][:144].strip())    # validation
#     tweet["timestamp"] = int(time.time())
#
#     query = """
#             INSERT INTO tweet (poster, content, timestamp)
#             VALUES ("{poster}", "{content}", {timestamp});
#             """.format(**tweet)

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
