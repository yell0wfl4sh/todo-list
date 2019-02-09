#!/usr/bin/python

import sqlite3
import os
if not os.path.isfile('./test.db'):
	with open("test.db", "w+") as f:
		conn = sqlite3.connect('test.db')
		print ("Opened database successfully")
		conn.execute('''CREATE TABLE NOTES
			(ID INTEGER PRIMARY KEY AUTOINCREMENT,
			TITLE           TEXT    NOT NULL,
			DUEDATE        DATETIME,
			COMMENTS           TEXT,
			STATUS          BOOLEAN);''')
		print ("Table created successfully")
		print ("Opened database successfully")
		conn.close()

conn = sqlite3.connect('test.db')

def add_entry(title, duedate, comment=""):
	query = "INSERT INTO NOTES (TITLE,DUEDATE,COMMENTS,STATUS) VALUES ('{}', '{}', '{}', 0)".format(title, duedate, comment)
	conn.execute(query)

def update_entry(id, title, duedate, comment, status):
	query = ("UPDATE NOTES SET TITLE = '{}', DUEDATE = '{}', COMMENTS = '{}', STATUS = '{}' WHERE ID = {}").format(title, duedate, comment, status, id)
	conn.execute(query)

def delete_entry(id):
	query = ("DELETE FROM NOTES WHERE ID = {}").format(id)
	conn.execute(query)

delete_entry(1)
conn.commit()
print "Records created successfully";
conn.close()
