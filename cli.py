import sqlite3
from tabulate import tabulate
import click
import main
from main import add_entry, update_entry, delete_entry, fetch_entries


"""
Setup connection with database
"""
conn = sqlite3.connect('db.sqlite3')


@click.group()
def cli():
	"CLI extension for to-do list app"
	pass

@cli.command()
@click.option('-d', '--date', help="Due date in yyyy-mm-dd", default="")
@click.option('-c', '--comment', help="Notes for the task", default="")
@click.argument('task', nargs=1, required=False, metavar="TASK")
def add(task, date, comment):
	"Add an task in the to-do list"
	if task is None:
		while not task or task.isspace():
			task = input("Enter the task to be added to the to-do list: ")
	if not date:
		date = input("Enter the date for the task completion (yyyy-mm-dd): ")
	if not comment:
		comment = input("Enter the notes for the task (if any): ")
	add_entry(task, date, comment)

@cli.command()
def edit():
	"Incomplete: Edit an task in the to-do list"
	pass

@cli.command()
def delete():
	"Incomplete: Delete an task in the to-do list"
	pass

@cli.command()
def tasks():
	"Display all the tasks added by the user"
	entries = fetch_entries()
	print(tabulate(entries, headers=['Task', 'Due Date', 'Notes'], tablefmt='orgtbl'))

"""
Close the connection with database
"""
conn.close()