import sqlite3

conn = sqlite3.connect('Restaurants.db')

c = conn.cursor()

# Create Table Restaruants under database
c.exectute('''
        CREATE TABLE Restaurants (
        id INTEGER,
        name TEXT,
        visitDate TEXT,
        reviews REAL,)
        ''')

conn.commit()


