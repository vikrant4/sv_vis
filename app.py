from flask import Flask, send_from_directory, g, jsonify
import os
import sqlite3


app = Flask(__name__)
DATABASE = 'sv.db'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(e):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def main():
    app.run(debug=True)


@app.route("/")
def index():
    return send_from_directory(
        os.path.dirname(__file__),
        "app_index.html"
    )


@app.route("/api/facility", methods=['GET'])
def facility_data():
    try:
        db = get_db()
        result = db.execute('SELECT * FROM facility WHERE facility.name IN(SELECT in_facility FROM transfer UNION SELECT out_facility FROM transfer) ORDER BY latitude DESC').fetchall()
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL ERROR:', e)
        return 'Error'


@app.route("/api/transfer", methods=['GET'])
def transfer_data():
    try:
        db = get_db()
        result = db.execute('SELECT * from transfer').fetchall()
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL ERROR:', e)
        return 'Error'


if __name__ == '__main__':
    main()
