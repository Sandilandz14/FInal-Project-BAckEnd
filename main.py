import sqlite3
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS


app = Flask(__name__)


def init_sqlite_db():

    conn = sqlite3.connect('mydata.db')
    print("database has opened")

    conn.execute("CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, addr TEXT, password TEXT)")
    print("Table was created")

    # conn.execute("CREATE TABLE IF NOT EXISTS products(userID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, addr TEXT, password TEXT)")
    # print("Table was created")

    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign-up/')
def add_user():
    return render_template('signup.html')

@app.route('/add-data/', methods=['POST'])
def add_new_record():
    try:
        name = request.form['fname']
        email = request.form['email']
        addr = request.form['addr']
        password = request.form['password']

        with sqlite3.connect('mydata.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users(name, email, addr, password) VALUES(?, ?, ?, ?)", (name, email, addr, password))
            con.commit()
            msg = name + " successfully added to the table."
    except Exception as e:
        con.rollback()
        msg = "Error occured in nsert operation " + str(e)
    finally:
        con.close()
        return jsonify(msg)

@app.route('/show-records/')
def list_users():
    try:
        with sqlite3.connect('mydata.db') as con:
            con.row_factory = dict_factory
            con = sqlite3.connect('mydata.db')
            cur = con.cursor()
            cur.execute("select * from users")

            rows = cur.fetchall()

    except Exception as e:
        print("Something happened when getting data from db:"+str(e))
    return jsonify(rows)

if __name__=='__main__':
    app.run(debug=True)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



