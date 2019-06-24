from flask import Flask, send_from_directory, g, jsonify, request
import os
import sqlite3


app = Flask(__name__)
DATABASE = 'sv.db'
facility_col_list = [
    'code',
    'name',
    'type',
    'region',
    'suburb',
    'state',
    'postcode',
    'active'
]
transfer_col_list = [
    'trno',
    'in_facility',
    'datetimein',
    'weightnett',
    'item_group',
    'item_name',
    'inout',
    'quantity',
    'volume',
    'density',
    'kg_per_item',
    'tot_tonnes',
    'out_facility'
]


def get_db():
    """Return connection to database"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(e):
    """Close connection to database"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def main():
    app.run(debug=True)


@app.route("/")
def index():
    """Server index.html"""
    return send_from_directory(
        os.path.dirname(__file__),
        "app_index.html"
    )


def query_filter_generator(arguments, col_list):
    """Generate SQL filters for available columns from request arguments"""
    if arguments.get('transfer_present') == 'on':
        query_filter = """ WHERE facility.name IN
        (SELECT in_facility from transfer
        UNION SELECT out_facility FROM transfer)"""
    else:
        query_filter = ''
    for col in col_list:
        if arguments.get(col):
            if arguments.get(col) == 'all':
                continue
            elif len(query_filter) == 0:
                query_filter = " WHERE {} = '{}'".format(
                    col, arguments.get(col))
            else:
                query_filter = query_filter + \
                    " AND {} = '{}'".format(col, arguments.get(col))
    return query_filter


@app.route("/api/facility", methods=['GET'])
def facility_data():
    """API to send facility data"""
    filter_query = query_filter_generator(
        request.args, facility_col_list)
    print('Filter query', filter_query)
    try:
        db = get_db()
        result = db.execute(
            "SELECT * FROM facility " + filter_query +
            """ ORDER BY latitude DESC""").fetchall()
        print(jsonify([dict(r) for r in result]))
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL ERROR:', e)
        return 'Error'


@app.route("/api/transfer", methods=['GET'])
def transfer_data():
    """API to send transfer data"""
    filter_query = query_filter_generator(request.args, transfer_col_list)
    print('Filter query', filter_query)
    try:
        db = get_db()
        result = db.execute('SELECT * from transfer' + filter_query).fetchall()
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL ERROR:', e)
        return 'Error'
    except Exception as e:
        print('ERROR:', e)
        return 'Error'


if __name__ == '__main__':
    main()
