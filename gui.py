#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
import main
from main import fetch_entries, add_entry
import sqlite3

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
        self.value = calendar.get_date()

class ToDoApp(Gtk.Window):
    """
    Main Class
    """
    def __init__(self):
        """ Intialise the window """
        Gtk.Window.__init__(self)
        self.set_title('To Do App')
        self.set_default_size(600, 900)
        self.set_border_width(10)
        self.dateval = "(year=2019, month=11, day=19)"
        mainbox = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)

        hbox1 = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
        hbox1.set_size_request(10, 40)
        hbox1.set_homogeneous(False)

        label = Gtk.Label("To Do App")
        hbox1.pack_start(label, True, True, 0)

        mainbox.add(hbox1)

        hbox2 = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
        hbox2.set_size_request(10, 40)
        hbox2.set_homogeneous(False)

        entry1 = Gtk.Entry()
        entry1.set_text("Enter Note Here")
        hbox2.pack_start(entry1, True, True, 0)

        entry2 = Gtk.Entry()
        entry2.set_text("Enter Comment Here")
        hbox2.pack_start(entry2, True, True, 0)

        cal_button = Gtk.Button()
        icon_cal = Gio.ThemedIcon(name="gnome-calendar")
        image_cal = Gtk.Image.new_from_gicon(icon_cal, Gtk.IconSize.BUTTON)
        cal_button.add(image_cal)
        cal_button.set_tooltip_text("Pick date")
        cal_button.connect("clicked", self.on_cal_clicked)
        hbox2.pack_start(cal_button, True, True, 0)

        addbutton = Gtk.Button.new_with_label("Add")
        addbutton.connect("clicked", self.add_note, entry1, entry2)
        hbox2.pack_start(addbutton, True, True, 0)
        
        mainbox.add(hbox2)

        listbox = Gtk.ListBox()
        listbox.set_size_request(10, 800)
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        all_entries = fetch_entries()
        for note in all_entries:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            hbox.set_homogeneous(True)
            row.add(hbox)

            for text in range(1, 5):
                label1 = Gtk.Label(note[text], xalign=0)
                hbox.pack_start(label1, True, True, 0)

            updatebutton = Gtk.Button.new_with_label("Update")
            updatebutton.connect("clicked", self.update_note)
            hbox.pack_start(updatebutton, True, True, 0)

            listbox.add(row)

        mainbox.add(listbox)
        self.add(mainbox)
        self.listbox = listbox

    def update_display(self):
        listbox = self.listbox
        elements = listbox.get_children()
        for note in elements:
            listbox.remove(note)
        all_entries = fetch_entries()
        for note in all_entries:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            hbox.set_homogeneous(True)
            row.add(hbox)

            for text in range(1, 5):
                label1 = Gtk.Label(note[text], xalign=0)
                hbox.pack_start(label1, True, True, 0)

            updatebutton = Gtk.Button.new_with_label("Update")
            updatebutton.connect("clicked", self.update_note)
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
        datetime = self.parse_date()
        add_entry(title.props.text, comment.props.text, datetime)
        self.update_display()

    def update_note(self, widget):
        """ Update existing note """
        pass

    def parse_date(self):
        vals = (self.dateval).split(',')
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

win = ToDoApp()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

