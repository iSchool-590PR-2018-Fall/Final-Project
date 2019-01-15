import json
import sqlite3
import os.path

# create database
def create_database(data, db):
	c = db.cursor()
	c.execute('CREATE TABLE personal_info (first_name varchar(20) , last_name varchar(20), gender, city, country, likes)')

	query = 'INSERT INTO personal_info (first_name, last_name, gender, city, country, likes) VALUES(?,?,?,?,?,?)'
	columns = ['first_name', 'last_name', 'gender', 'city', 'country', 'likes']

	for key, value in data.items():
			keys = tuple(value[c] for c in columns)
			# print(keys)
			c = db.cursor()
			c.execute(query, keys)
			c.close() 

	db.commit()
	db.close()  


# retrieve data from database
if os.path.isfile('data.db') == False:
	data = json.load(open('data.json'))
	db = sqlite3.connect('data.db')
	create_database(data, db)
else:
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	print("first_name, last_name, gender, city, country, likes\n")
	for row in cursor.execute('select * from personal_info; '):
		print(row)
	cursor.close()