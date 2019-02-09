#!/usr/bin/python

import sqlite3
import os
import logging

"""
Configuration for the Logger
"""
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

"""
Create a database along with the table if the database is not present
"""
if not os.path.isfile('./db.sqlite3'):
	with open("db.sqlite3", "w+") as f:
		conn = sqlite3.connect('db.sqlite3')
		logging.info("Opened database successfully")
		conn.execute('''CREATE TABLE NOTES
					(ID INTEGER PRIMARY KEY AUTOINCREMENT,
					TITLE TEXT NOT NULL,
					DUEDATE DATETIME,
					COMMENTS TEXT,
					STATUS BOOLEAN);''')
		logging.info("Table created successfully")
		conn.close()


"""
Setup connection with database
"""
conn = sqlite3.connect('db.sqlite3')

logging.debug("Database connection successful")

def add_entry(title, duedate="", comment=""):
	""" Add a task in the database """
	logging.debug("Adding an entry in the database!")
	query = f"INSERT INTO NOTES (TITLE,DUEDATE,COMMENTS,STATUS) VALUES ('{title}', '{duedate}', '{comment}', 0)"
	conn.execute(query)

def update_entry(id, title, duedate, comment, status):
	""" Update a task in the database """
	logging.debug("Updating an entry in the database!")
	query = f"UPDATE NOTES SET TITLE = '{title}', DUEDATE = '{duedate}', COMMENTS = '{comment}', STATUS = '{status}' WHERE ID = {id}"
	conn.execute(query)

def delete_entry(id):
	""" Delete a task from the database """
	logging.debug("Deleting an entry from the database!")
	query = f"DELETE FROM NOTES WHERE ID = {id}"
	conn.execute(query)

def fetch_entries():
	""" Fetch the tasks from the database """
	logging.debug("Fetching entries from the database!")
	query = "SELECT * from NOTES"
	cursor = conn.execute("SELECT * from NOTES")
	for row in cursor:
		logging.debug(f"TASK = {row[1]}")
		logging.debug(f"DATE = {row[2]}")
		logging.debug(f"COMMENTS = {row[3]}")

conn.commit()
"""
Close the connection with database
"""
conn.close()
