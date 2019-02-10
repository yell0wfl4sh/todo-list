#!/usr/bin/python

import sqlite3
import os
import logging

import click

"""
Configuration for the Logger
"""
logging.basicConfig(level=logging.INFO, format='%(message)s')


def success(msg):
    """ Returns enhanced input """
    return click.secho(msg, fg='green')

"""
Create a database along with the table if the database is not present
"""
if not os.path.isfile('./db.sqlite3'):
	with open("db.sqlite3", "w+") as f:
		conn = sqlite3.connect('db.sqlite3')
		success("Opened database successfully")
		conn.execute('''CREATE TABLE NOTES
					(ID INTEGER PRIMARY KEY AUTOINCREMENT,
					TITLE TEXT NOT NULL,
					DUEDATE DATETIME,
					COMMENTS TEXT,
					STATUS BOOLEAN);''')
		success("Table created successfully")
		conn.close()


logging.debug("Database connection successful")

def add_entry(title, duedate="", comment=""):
	""" Add a task in the database """
	logging.debug("Adding an entry in the database!")
	""" Setup connection with database """
	conn = sqlite3.connect('db.sqlite3')
	query = f"INSERT INTO NOTES (TITLE,DUEDATE,COMMENTS,STATUS) VALUES ('{title}', '{duedate}', '{comment}', 0)"
	conn.execute(query)
	success("Successfully added a task in the database")
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
	success("Successfully updated a task in the database")
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
	success("Successfully deleted a task from the database")
	""" Commit the changes and close connection with the database """
	conn.commit()
	conn.close()

def fetch_entry(id):
	""" Fetch a particular task from the database """
	""" Setup connection with database """
	conn = sqlite3.connect('db.sqlite3')
	logging.debug("Fetching an entry from the database!")
	query = f"SELECT * from NOTES WHERE ID={id}"
	cursor = conn.execute(query)
	entry = cursor.fetchone()
	conn.commit()
	conn.close()
	return entry

def fetch_entries():
	""" Fetch the tasks from the database """
	""" Setup connection with database """
	conn = sqlite3.connect('db.sqlite3')
	logging.debug("Fetching entries from the database!")
	query = "SELECT * from NOTES"
	cursor = conn.execute(query)
	entries = []
	for row in cursor:
		entry = []
		entry.append(row[0])
		entry.append(row[1])
		entry.append(row[2])
		entry.append(row[3])
		if row[4] == 1:
			status = "Done"
		else:
			status= "Not Done"
		entry.append(status)
		entries.append(entry)
	""" Commit the changes and close connection with the database """
	conn.commit()
	conn.close()
	return entries
