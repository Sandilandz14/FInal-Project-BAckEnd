import sqlite3
from flask import Flask, render_template, request


def init_sqlite_db():

    conn = sqlite3.connect('mydata.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS students(name TEXT, addr TEXT, city TEXT, pin TEXT)")
    print("Table created successfully")
    conn.close()

    init_sqlite_db()
