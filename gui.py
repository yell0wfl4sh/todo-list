#!/usr/bin/python

import gi
import main
import sqlite3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio
from main import fetch_entries, add_entry, fetch_entry, update_entry

class CalDialog(Gtk.Dialog):
    """
    Calendar Dialog
    """
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Select Date", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
 
        self.set_default_size(300, 200)
        self.value = None
        box = self.get_content_area()
 
        calendar = Gtk.Calendar()
        calendar.set_detail_height_rows(1)
        calendar.set_property("show-details",True)
        calendar.set_detail_func(self.cal_entry)
 
        box.add(calendar)
        self.show_all()
 
    def cal_entry(self, calendar, year, month, date):
        """ Updates the value when selected """
        self.value = calendar.get_date()

class UpdateDialog(Gtk.Dialog):

    def __init__(self, parent, id):
        """
        Dialog for updating an entry
        """
        Gtk.Dialog.__init__(self, "Update Value", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(300, 200)
        note = fetch_entry(id)
        box = self.get_content_area()

        title_entry = Gtk.Entry()
        title_entry.set_text(note[1])
        box.pack_start(title_entry, True, True, 0)

        comment_entry = Gtk.Entry()
        comment_entry.set_text(note[3])
        box.pack_start(comment_entry, True, True, 0)

        hbox = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_homogeneous(True)

        vbox1 = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        cal_button = Gtk.Button()
        icon_cal = Gio.ThemedIcon(name="gnome-calendar")
        image_cal = Gtk.Image.new_from_gicon(icon_cal, Gtk.IconSize.BUTTON)
        cal_button.add(image_cal)
        cal_button.set_tooltip_text("Pick date")
        cal_button.connect("clicked", self.on_cal_clicked)
        vbox1.pack_start(cal_button, True, True, 0)
        hbox.add(vbox1)

        vbox2 = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        checkbut = Gtk.CheckButton("Status")
        if(note[4]):
            checkbut.set_active(True)
        checkbut.connect("toggled", self.on_checked, checkbut)
        vbox2.pack_start(checkbut, True, True, 0)

        hbox.add(vbox2)
        box.add(hbox)

        """ These attributes are used for getting value while executing update function """
        self.title = title_entry
        self.comment = comment_entry
        self.dateval = note[2]
        self.status = note[4]
        self.show_all()

    def on_checked(self, widget, checkbut):
        """ Update attribute when state is changed """
        if checkbut.get_active():
            self.status = 1
        else:
            self.status = 2

    def on_cal_clicked(self, widget):
        """ Open calender and get user selection """
        dialog = CalDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.dateval = str(dialog.value)
        dialog.destroy()

class ToDoApp(Gtk.Window):
    """
    Main Class
    """
    def __init__(self):
        """ Intialise main window """
        Gtk.Window.__init__(self)
        self.set_title('To Do App')
        self.set_default_size(910, 900)
        self.set_border_width(10)
        self.dateval = "(year=2019, month=02, day=10)"

        """ Main GtkBox : Contains three HBox as child """
        mainbox = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)

        heading_hbox = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
        heading_hbox.set_size_request(10, 40)
        heading_hbox.set_homogeneous(False)

        label = Gtk.Label("To Do App")
        heading_hbox.pack_start(label, True, True, 0)

        mainbox.add(heading_hbox)

        """ GtkBox which takes input """
        input_hbox = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
        input_hbox.set_size_request(10, 40)
        input_hbox.set_homogeneous(False)

        title_entry = Gtk.Entry()
        title_entry.set_text("Enter Note Here")
        input_hbox.pack_start(title_entry, True, True, 0)

        comment_entry = Gtk.Entry()
        comment_entry.set_text("Enter Comment Here")
        input_hbox.pack_start(comment_entry, True, True, 0)

        cal_button = Gtk.Button()
        icon_cal = Gio.ThemedIcon(name="gnome-calendar")
        image_cal = Gtk.Image.new_from_gicon(icon_cal, Gtk.IconSize.BUTTON)
        cal_button.add(image_cal)
        cal_button.set_tooltip_text("Pick date")
        cal_button.connect("clicked", self.on_cal_clicked)
        input_hbox.pack_start(cal_button, True, True, 0)

        addbutton = Gtk.Button.new_with_label("Add")
        addbutton.connect("clicked", self.add_note, title_entry, comment_entry)
        input_hbox.pack_start(addbutton, True, True, 0)
        
        mainbox.add(input_hbox)

        """ GtkBox to add notes in ListBox """
        listbox = Gtk.ListBox()
        listbox.set_size_request(10, 800)
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        """ Add header row for all notes """
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        hbox.set_homogeneous(True)
        row.add(hbox)
        row.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("grey"))
        row.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))
        row.set_size_request(10, 40)
        heading = ("Title", "Date","Comment", "Status", "")
        for text in heading:
            label = Gtk.Label(text, xalign=0)
            hbox.pack_start(label, True, True, 0)

        listbox.add(row)

        """ Add rows for all notes """
        all_entries = fetch_entries()
        for note in all_entries:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            hbox.set_homogeneous(True)
            row.add(hbox)

            for text in range(1, 5):
                label = Gtk.Label(note[text], xalign=0)
                hbox.pack_start(label, True, True, 0)

            updatebutton = Gtk.Button.new_with_label("Update")
            updatebutton.connect("clicked", self.update_note, note[0])
            hbox.pack_start(updatebutton, True, True, 0)

            listbox.add(row)

        mainbox.add(listbox)
        self.add(mainbox)
        self.listbox = listbox

    def update_display(self):
        """ Update notes displayed on the main screen """
        listbox = self.listbox
        elements = listbox.get_children()
        for note in range(1, len(elements)):
            listbox.remove(elements[note])
        all_entries = fetch_entries()
        for note in all_entries:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            hbox.set_homogeneous(True)
            row.add(hbox)

            for text in range(1, 5):
                label = Gtk.Label(note[text], xalign=0)
                hbox.pack_start(label, True, True, 0)

            updatebutton = Gtk.Button.new_with_label("Update")
            updatebutton.connect("clicked", self.update_note, note[0])
            hbox.pack_start(updatebutton, True, True, 0)

            listbox.add(row)

        listbox.show_all()

    def on_cal_clicked(self, widget):
        """ Open calender and get user selection """
        dialog = CalDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.dateval = str(dialog.value)
        dialog.destroy()

    def add_note(self, widget, title, comment):
        """ Add new note """
        datetime = self.parse_date(self.dateval)
        add_entry(title.props.text, datetime, comment.props.text)
        self.update_display()

    def update_note(self, widget, id):
        """ Update existing note """
        dialog = UpdateDialog(self, id)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            datetime = self.parse_date(dialog.dateval)
            update_entry(id, dialog.title.props.text,
                datetime, dialog.comment.props.text, dialog.status)
            self.update_display()
        dialog.destroy()


    def parse_date(self, dateval):
        """ Get date in desired format """
        if len(dateval)>10:
            vals = (dateval).split(',')
            datetime = vals[0][-4:]
            if(len(vals[1])==8):
                datetime = datetime + "-0" + vals[1][-1:]
            else:
                datetime = datetime + "-" +  vals[1][-2:]

            if(len(vals[2])==7):
                datetime = datetime + "-0" + vals[2][-2:-1]
            else:
                datetime = datetime + "-" + vals[2][-3:-1]
            return datetime
        else:
            return dateval

win = ToDoApp()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

