#!/usr/bin/python

import sqlite3
import os
import logging

"""
Configuration for the Logger
"""
logging.basicConfig(level=logging.INFO, format='%(message)s')

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


logging.debug("Database connection successful")

def add_entry(title, duedate="", comment=""):
	""" Add a task in the database """
	logging.debug("Adding an entry in the database!")
	""" Setup connection with database """
	conn = sqlite3.connect('db.sqlite3')
	query = f"INSERT INTO NOTES (TITLE,DUEDATE,COMMENTS,STATUS) VALUES ('{title}', '{duedate}', '{comment}', 0)"
	conn.execute(query)
	logging.info("Successfully added a task in the database")
	""" Commit the changes and close connection with the database """
	conn.commit()
	conn.close()

def update_entry(id, title, duedate, comment, status):
	""" Update a task in the database """
	logging.debug("Updating an entry in the database!")
	""" Setup connection with database """
	conn = sqlite3.connect('db.sqlite3')
	query = f"UPDATE NOTES SET TITLE = '{title}', DUEDATE = '{duedate}', COMMENTS = '{comment}', STATUS = '{status}' WHERE ID = {id}"
	conn.execute(query)
	logging.info("Successfully updated a task in the database")
	""" Commit the changes and close connection with the database """
	conn.commit()
	conn.close()

def delete_entry(id):
	""" Delete a task from the database """
	logging.debug("Deleting an entry from the database!")
	""" Setup connection with database """
	conn = sqlite3.connect('db.sqlite3')
	query = f"DELETE FROM NOTES WHERE ID = {id}"
	conn.execute(query)
	logging.info("Successfully deleted a task from the database")
	""" Commit the changes and close connection with the database """
	conn.commit()
	conn.close()

def fetch_entries():
	""" Fetch the tasks from the database """
	""" Setup connection with database """
	conn = sqlite3.connect('db.sqlite3')
	logging.debug("Fetching entries from the database!")
	query = "SELECT * from NOTES"
	cursor = conn.execute("SELECT * from NOTES")
	entries = []
	for row in cursor:
		entry = []
		logging.debug(f"ID = {row[0]}")
		entry.append(row[0])
		logging.debug(f"TASK = {row[1]}")
		entry.append(row[1])
		logging.debug(f"DATE = {row[2]}")
		entry.append(row[2])
		logging.debug(f"COMMENTS = {row[3]}")
		entry.append(row[3])
		entries.append(entry)
	""" Commit the changes and close connection with the database """
	conn.commit()
	conn.close()
	return entries
