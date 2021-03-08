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

    conn.execute("CREATE TABLE IF NOT EXISTS products(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, reviews TEXT, description TEXT, price TEXT, image TEXT)")
    print("Products was created")

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
        msg = "Error occured in insert operation " + str(e)
    finally:
        con.close()
        return {'msg': msg}


@app.route('/show-records/', methods=['GET'])
def list_users():
    try:
        with sqlite3.connect('mydata.db') as con:
            con.row_factory = dict_factory
            # con = sqlite3.connect('mydata.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()

    except Exception as e:
        print("Something happened when getting data from db:"+str(e))
    return jsonify(rows)


# @app.route('/products/', methods = ['POST'])
# def insert_products():
#     with sqlite3.connect('mydata.db') as con:
#         con.row_factory = dict_factory
#         cur = con.cursor()
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('almonds', 'Rated: 4.0/5', '250g Almonds.\n','Available:  R80', 'https://i.postimg.cc/nrTDk302/almonds.jpg')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('black sesame seeds', 'Rated: 4.6/5', '400g Black Sesame Seeds.\n','Available:  R120', 'https://i.postimg.cc/kXVxX1hB/back-Sesameseeds.jpg')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('chia seeds', 'Rated: 4.3/5', '1KG Chia Seeds.\n', 'Available:  R200', 'https://i.postimg.cc/9MYj9Y89/chiaseeds.jpg')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('mixed nuts', 'Rated: 4.0/5', '1KG Mixed Nuts.\n', 'Available: R220', 'https://i.postimg.cc/NjC8shQ9/mixednuts.jpg')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('pumpkin seeds', 'Rated: 3.9/5', '750g Pumpkin Seeds.\n','Available:  R170', 'https://i.postimg.cc/vHVwLyNM/pumpkinseeds.jpg')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('cashew nuts', 'Rated: 4.5/5', '1KG Cashew Nuts.\n','Available:  R185', 'https://i.postimg.cc/KzfBHCp8/cashewnuts1.jpg')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('dried peaches', 'Rated: 4.2/5', '500g Dried Peaches.\n','Available:  R90', 'https://i.postimg.cc/wBZD8hgS/driedpeaches.png')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('pecan nut halves', 'Rated: 4.0/5', '1KG Pecan Nut Halves.\n','Available:  R275', 'https://i.postimg.cc/7YysWtM8/pecan.png')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('peanuts', 'Rated: 4.3/5', '1KG Peanuts.\n','Available:  R120', 'https://i.postimg.cc/Pr2xR9sP/peanuts.png')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('cranberries dried', 'Rated: 4.9/5', '1KG Cranberries Dried.\n','Available:  R180', 'https://i.postimg.cc/63vW9V6Z/cranberries.png')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('sunflower seeds', 'Rated: 3.7/5', '1KG Sunflower Seeds.\n','Available:  R140', 'https://i.postimg.cc/Nf5MZbgD/sunflowerseeds.png')")
#         cur.execute("INSERT INTO products(name, reviews, description, price, image) VALUES('hazelnuts', 'Rated: 4.0/5', '1KG Hazelnuts.\n','Available:  R280', 'https://i.postimg.cc/tgt0Drg2/hazelnuts.png')")
#         con.commit()
# insert_products()



@app.route('/show-products/', methods= ['GET'])
def show_products():
    data = []
    try:
        with sqlite3.connect('mydata.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute('SELECT * FROM products')
            data = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching products from the database")
    finally:
        con.close()
        return jsonify(data)


if __name__=='__main__':
    app.run(debug=True)






