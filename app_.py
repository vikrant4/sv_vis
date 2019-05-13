#!/usr/bin/env python
# coding: utf-8

# In[84]:


from flask import Flask, send_from_directory, g, jsonify, request, render_template
import os
import sqlite3

# In[85]:


app = Flask(__name__)
DATABASE = 'sv.db'


# In[86]:


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


# In[87]:


@app.teardown_appcontext
def close_db(e):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# In[88]:


def main():
    app.run(debug=True)


# In[89]:


@app.route("/")
def index():
    return send_from_directory(
        os.path.dirname(__file__),
        "app_index.html"
    )
def request():
    if request.method = 'GET':
            return render_template('app_index.html')


# In[90]:


@app.route("/api/facility", methods=['GET'])
def facility_data():
    try:
        db = get_db()
        result = db.execute('SELECT * FROM facility WHERE facility.name IN(SELECT in_facility FROM transfer UNION SELECT out_facility FROM transfer) ORDER BY latitude DESC').fetchall()
        if not request.values.get("Landfill"):
            raise RuntimeError("Select Facility Type")
        if not request.values.get("Reprocessor"):
            raise RuntimeError("Select Facility Type")
        if not request.values.get("RRC/TS"):
            raise RuntimeError("Select Facility Type")
        type = request.values('ftype')
        db.execute("SELECT * FROM facility WHERE ftype={type}".\format(type=type))
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL ERROR:', e)
        return 'Error'


# In[91]:


@app.route("/api/transfer", methods=['GET'])
def transfer_data():
    try:
        db = get_db()
        result = db.execute('SELECT * from transfer').fetchall()
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL ERROR:', e)
        return 'Error'


# In[92]:


@app.route("/", methods = ['GET'])
def filter_facility():
    try:
        db = get_db()
        result = db.execute('SELECT * from facility WHERE ftype="Landfill"').fetchmany()
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL Error', e)
        return 'Error'
    
    try:
        db = get_db()
        result = db.execute('SELECT * from facility WHERE ftype="Reprocessor"').fetchmany()
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL Error', e)
        return 'Error'
    
    try:
        db = get_db()
        result = db.execute('SELECT * from facility WHERE ftype="RRC/TS"').fetchmany()
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL Error', e)
        return 'Error'


# In[ ]:


@app.route("/", methods = ['GET'])
def filter_transfer():
    try:
        db = get_db()
        result = db.execute('SELECT * from transfer WHERE ftype="IN"').fetchmany()
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL Error', e)
        return 'Error'
    
    try:
        db = get_db()
        result = db.execute('SELECT * from transfer WHERE ftype="OUT"').fetchmany()
        return jsonify([dict(r) for r in result])
    except sqlite3.ProgrammingError as e:
        print('SQL Error', e)
        return 'Error'


# In[93]:


if __name__ == '__main__':
    app.run()


# In[ ]:





# In[ ]:




