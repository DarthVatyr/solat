import sqlite3

with sqlite3.connect("sample.db") as connection:
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE posts(title TEXT, description TEXT)')
    cursor.execute('INSERT INTO posts VALUES("title1", "description1")')
    cursor.execute('INSERT INTO posts VALUES("title2", "description2")')
    cursor.execute('INSERT INTO posts VALUES("title3", "description3")')