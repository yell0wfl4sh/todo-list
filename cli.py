import sys
import sqlite3

from tabulate import tabulate
import click
import main
from main import add_entry, update_entry, delete_entry, fetch_entry, fetch_entries

def cli_input(msg):
    """ Returns enhanced input """
    return input(click.style(msg, fg='cyan'))

""" Setup Command Group """
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
			task = cli_input("Enter the task to be added to the to-do list: ")
	if not date:
		date = cli_input("Enter the date for the task completion (yyyy-mm-dd): ")
	if not comment:
		comment = cli_input("Enter the notes for the task (if any): ")
	add_entry(task, date, comment)

@cli.command()
@click.option('-t', '--task', help="Updated description of the task")
@click.option('-d', '--date', help="Updated due date in yyyy-mm-dd")
@click.option('-c', '--comment', help="Updated notes for the task")
@click.argument('id', nargs=1, required=False, metavar="ID")
def update(id, task, date, comment):
	"Edit an task in the to-do list"
	if id is None:
		entries = fetch_entries()
		click.secho(tabulate(entries, headers=['ID', 'Task', 'Due Date', 'Notes', 'Status'], tablefmt='orgtbl'), fg='yellow')
		while not id or id.isspace():
			id = cli_input("Enter the ID of the task to be updated: ")
	entry = fetch_entry(id)
	if entry is None:
		click.secho("Invalid ID", fg='red')
		sys.exit()
	if task is None:
		task = cli_input("Enter a new description for task (if you wish to update): ")
	if not task or task.isspace():
		task = entry[1]
	if date is None:
		date = cli_input("Enter a new date for task completion (if you wish to update) (yyyy-mm-dd): ")
	if not date or date.isspace():
		date = entry[2]
	if comment is None:
		comment = cli_input("Enter a new comment for task (if you wish to update): ")
	if not comment or comment.isspace():
		comment = entry[3]
	status = int(cli_input("Enter a new status for task (if you wish to update) (0/1): "))
	update_entry(id, task, date, comment, status)


@cli.command()
def delete():
	"Incomplete: Delete an task in the to-do list"
	pass

@cli.command()
def show():
	"Display all the tasks added by the user"
	entries = fetch_entries()
	click.secho(tabulate(entries, headers=['ID', 'Task', 'Due Date', 'Notes', 'Status'], tablefmt='orgtbl'), fg='yellow')


if __name__ == '__main__':
	cli()
