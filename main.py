import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init_sqlite_db():

    conn = sqlite3.connect('mydata.db')
    print("database has opened")

    conn.execute("CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, addr TEXT, password TEXT)")
    print("Users table was created")

    # conn.execute("CREATE TABLE IF NOT EXISTS products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT)")
    # print("Products was created")



    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    print(cur.fetchall())
init_sqlite_db()


@app.route('/add-data/', methods=['POST'])
def add_new_record():
    if request.method == 'POST':
        msg = None
    try:
        post_data = request.get_json()
        name = post_data['name']
        email = post_data['email']
        addr = post_data['addr']
        password = post_data['password']

        with sqlite3.connect('mydata.db') as con:
            cur = con.cursor()
            con.row_factory=dict_factory
            cur.execute("INSERT INTO users(name, email, addr, password) VALUES(?, ?, ?, ?)", (name, email, addr, password))
            con.commit()
            msg = name + " successfully added to the table."
    except Exception as e:
        con.rollback()
        msg = "Error occured insert operation " + str(e)
    finally:
        con.close()
        return {'msg': msg}

@app.route('/show-records/', methods=['GET'])
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

# @app.route('/products/')
# def insert_products():
#     try:
#         with sqlite3.connect('mydata.db') as con:
#             con.row_factory = dict_factory
#             cur = con.cursor()
#             cur.execute("INSERT INTO products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT) VALUES( 1, almonds, 4/5, Well made almonds. Good for the soul., R200, https://i.postimg.cc/nrTDk302/almonds.jpg)")
#             cur.execute("INSERT INTO products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT) VALUES()")
#             cur.execute("INSERT INTO products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT) VALUES()")
#             cur.execute("INSERT INTO products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT) VALUES()")
#             cur.execute("INSERT INTO products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT) VALUES()")
#             cur.execute("INSERT INTO products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT) VALUES()")
#             cur.execute("INSERT INTO products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT) VALUES()")
#             cur.execute("INSERT INTO products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT) VALUES()")
#             cur.execute("INSERT INTO products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT) VALUES()")
#             con.commit()
#             msg= 'Record successfully added.'
#     except Exception as e:
#         con.rollback()
#         msg = 'Error occurred in insert operation'+str(e)
#     finally:
#     con.close()
#     return jsonify(msg)


if __name__=='__main__':
    app.run(debug=True)






