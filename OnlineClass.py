import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import *
import sys
import pickle  # Store and load data locally in the form of bytestream
import os
import time
import webbrowser
import requests  # For updates (File reading)
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from win10toast import ToastNotifier
from configparser import ConfigParser  # Reading .ini file for settings

'''
Settings:
    Option to choose what day is the first in the week.
    Option to set whether users must be prompted to check for updates everytime they open OCH.
    Option to set whether they want notifications for classes.
'''
'''
Next update: While adding classes, add a unique key to the front of the data file for the application to detect
if the loaded file is valid and contains classes. This is to prevent users from loading random txt or dat files and 
corrupting system_values path.

Added feature to close program with Control + W
Added feature to load only valid files
'''

__author__ = 'Rahul Maddula'
__copyright__ = 'Copyright (C) 2021, Ravens Enterprises'
__credits__ = ['Rahul Maddula']
__license__ = 'GNU General Public License v3.0'
__version__ = "1.0.1"
__maintainer__ = 'Rahul Maddula'
__email__ = 'vensr.maddula@gmail.com'
__AppName__ = 'OCH'

# update the code with states of updateclass button
now = datetime.now()  # Doesn't update with change of time. Uses same value from the time of execution.
today = date.today().weekday()  # 0 is Monday and 6 is Sunday
current_time = time.strftime("%H:%M:%S")
record_no = -1  # Default variable
# use lists to store and load data on the disk with pickle module.


def close():
    root.destroy()


root = tk.Tk()
root.bind("<Control-w>", lambda x: close())  # Close OCH on pressing Control + W
root.iconbitmap("images/OCH_Logo.ico")
root.grid_columnconfigure(0, weight=200)
root.grid_rowconfigure(0, weight=200)
style = ttk.Style()

# Menu
menu1 = Menu(root)
root.config(menu=menu1)


def homemenu():
    for frame in frames:
        if frame != frame1 and frame != frame6:
            frame.place_forget()
    frame6.place(relwidth=0.18, relheight=0.2, relx=0.8,
                 rely=0.05)
    frame1.grid(pady=0, padx=0)
    frame1.place(relwidth=1, relheight=1, relx=0, rely=0)


def classesmenu():
    for frame in frames:
        if frame != frame2 and frame != frame5:
            frame.place_forget()
    frame2.grid(pady=0, padx=0)
    frame2.place(relwidth=1, relheight=1, relx=0, rely=0)
    frame5.place(relx=0.05, rely=0.42, relwidth=0.96, relheight=0.4)


def aboutmenu():
    for frame in frames:
        if frame != frame3:
            frame.place_forget()
    frame3.grid(pady=0, padx=0)
    frame3.place(relwidth=1, relheight=1, relx=0, rely=0)


def updatesmenu():
    for frame in frames:
        if frame != frame7:
            frame.place_forget()
    frame7.grid(pady=0, padx=0)
    frame7.place(relwidth=1, relheight=1, relx=0, rely=0)


def helpmenu():
    for frame in frames:
        if frame != frame4:
            frame.place_forget()
    frame4.grid(pady=0, padx=0)
    frame4.place(relwidth=1, relheight=1, relx=0, rely=0)


def settingsmenu():
    for frame in frames:
        if frame != frame8:
            frame.place_forget()
    frame8.grid(pady=0, padx=0)
    frame8.place(relwidth=1, relheight=1, relx=0, rely=0)


def feedbackmenu():
    for frame in frames:
        if frame != frame9:
            frame.place_forget()
    frame9.grid(pady=0, padx=0)
    frame9.place(relwidth=1, relheight=1, relx=0, rely=0)


# Menu items
home = Menu(menu1, tearoff=0)  # Tear-off 0 removes the dashed lines in the menu which opens menu items in another window
classtab = Menu(menu1, tearoff=0)
Options = Menu(menu1, tearoff=0)
helptab = Menu(menu1, tearoff=0)

menu1.add_cascade(label="Home", menu=home)
home.add_command(label="Go to Online Class Helper", command=homemenu)

menu1.add_cascade(label="Classes", menu=classtab)
classtab.add_command(label="View/Edit Classes", command=classesmenu)

menu1.add_cascade(label="Options", menu=Options)
Options.add_command(label="Settings", command=settingsmenu)

menu1.add_cascade(label="Help", menu=helptab)
helptab.add_command(label="Updates", command=updatesmenu)
helptab.add_command(label="Contact", command=helpmenu)
helptab.add_command(label="Send Feedback", command=feedbackmenu)
helptab.add_command(label="About Online Class Helper", command=aboutmenu)

# Canvas
canvas = tk.Canvas(root, height=root.winfo_screenheight(), width=root.winfo_screenwidth(), bg="black")
canvas.grid(sticky=N + E + W + S, column=0, pady=0, padx=0)
canvas.grid_rowconfigure(0, weight=1)
canvas.grid_columnconfigure(0, weight=1)

# Mainframe
frame1 = tk.Frame(root, bg="black")  # Frame placed inside the canvas. Same colour as canvas so invisible.
frame1.grid(sticky=N + E + W + S, row=0, column=0, pady=0, padx=0)
frame1.grid_rowconfigure(0, weight=1)
frame1.grid_columnconfigure(0, weight=1)
frame1.place(relwidth=1, relheight=1)

# Other frames
frame2 = Frame(root, bg="black")  # Classes
frame3 = Frame(root, bg="black")  # About
frame4 = Frame(root, bg="black")  # Help
frame6 = tk.Frame(frame1, bg="#2B2B26")  # Next Class
frame6.place(relwidth=0.18, relheight=0.2, relx=0.8,
             rely=0.05)
frame7 = Frame(root, bg="black")  # Updates
frame8 = Frame(root, bg="black")  # Settings
frame9 = Frame(root, bg="black")  # Feedback

root.title('Online Class Helper')  # Text to display on the title bar of the application
root.state('zoomed')  # Opens the maximised version of the window by default


# Data

system_in = open("data/settings.dat", "rb")
settings = pickle.load(system_in)
system_in.close()
data = settings['data_location']


# [day, [subject, start_time, end_time, class_link]]
# Uncomment the below code to fill the data file with an empty template
'''
classes_empty = [
    [0, [1]],
    [1, []],
    [2, []],
    [3, []],
    [4, []],
    [5, []],
    [6, []]
]
pickle_out = open(data, "wb")
pickle.dump(classes_empty, pickle_out)
pickle_out.close()
'''

'''
settings = {'data_location': 'data/data.dat', 'day': 1, 'prompt': True, 'notifications': True}
system_out = open("data/settings.dat", "wb")
pickle.dump(settings, system_out)
system_out.close()
'''

pickle_in = open(data, "rb")
classes = pickle.load(pickle_in)
pickle_in.close()


# Functions

def check_updates(close):  # close variable is to differentiate from button call and automatic prompt at startup
    try:
        response = requests.get(
            'https://raw.githubusercontent.com/vens8/Online-Class-Helper-Windows/main/VERSION.txt')
        latest = response.text.partition('\n')[0]  # Because GitHub appends an empty line at the end
        if latest > __version__:
            messagebox.showinfo('Software Update', 'Update Available!')
            toupdate = messagebox.askyesno('Update Available',
                                           f'{__AppName__} {__version__} needs to update to version {latest}')
            if toupdate is True:
                webbrowser.open_new_tab(
                    'https://github.com/vens8/Online-Class-Helper-Windows/blob/main/OCH_setup.exe?raw=true')
                root.destroy()
        else:
            if close == 1:
                messagebox.showinfo('Software Update',
                                    f"No updates available. You're using the latest version.\n{__AppName__} {__version__}")
    except Exception as e:
        messagebox.showinfo('Error Updating', 'Unable to check for update, please check your internet connection!')


if settings['prompt']:
    check_updates(0)


def load_file():
    global data, classes, settings
    filetypes = (
        ('DAT files', '*.dat'),
        ('text files', '*.txt')
    )
    temp_data = fd.askopenfilename(filetypes=filetypes)  # Store in temporary variable to not disturb 'data' global.
    if len(temp_data) > 0:
        try:
            pickle_in = open(temp_data, "rb")
            temp_classes = pickle.load(pickle_in)
            pickle_in.close()
            if isinstance(temp_classes, list) and len(temp_classes) == 7:
                data = temp_data
                system_out = open("data/settings.dat", "wb")  # Change the value in the DAT file
                settings['data_location'] = data  # Update the location of data file
                pickle.dump(settings, system_out)
                system_out.close()
                pickle_in = open(data, "rb")
                classes = pickle.load(pickle_in)
                pickle_in.close()
                fill_table()
            else:
                messagebox.showinfo('Invalid file',
                                    "The file you're trying to load is not supported. Try loading another file.")
        except IndexError:
            print("No file selected.")
    else:
        print("No file selected.")


def sortRecords():
    global classes, data
    for record in classes:
        record[1].sort(key=lambda x: x[1])
    pickle_out = open(data, "wb")  # updates the dat file with sorted records
    pickle.dump(classes, pickle_out)
    pickle_out.close()


def live_status():
    message2.config(text=live_status2())
    global classes, data
    pickle_in = open(data, "rb")  # reads the dat file for records
    classes = pickle.load(pickle_in)
    pickle_in.close()
    if len(classes) == 0 or (len(classes[0][1]) == 0 and len(classes[1][1]) == 0 and len(classes[2][1]) == 0 and len(
            classes[3][1]) == 0 and len(classes[4][1]) == 0 and len(classes[5][1]) == 0 and len(classes[6][1]) == 0):
        status = "You haven't set up any classes yet.\nPlease add them in the 'Classes' tab."
        return status
    else:
        current_time = time.strftime("%H:%M:%S")
        for i in classes:
            if today == i[0]:
                for j in i[1]:
                    if current_time >= j[1] and current_time < j[2]:
                        status = f"Current class:        {j[0]}\nStart time:            {j[1]}\nEnd time:              {j[2]}\n"
                        return status
                status = f"No ongoing class currently"
                return status
        status = f"No ongoing class currently"
        return status


def live_status2():
    global classes, data
    pickle_in = open(data, "rb")  # reads the dat file for records
    classes = pickle.load(pickle_in)
    pickle_in.close()
    if len(classes) == 0 or (len(classes[0][1]) == 0 and len(classes[1][1]) == 0 and len(classes[2][1]) == 0 and len(
            classes[3][1]) == 0 and len(classes[4][1]) == 0 and len(classes[5][1]) == 0 and len(classes[6][1]) == 0):
        status = "Setup incomplete"
        button9['state'] = 'disabled'
        return status
    else:
        current_time = time.strftime("%H:%M:%S")
        for i in classes:
            if today == i[0]:
                for j in i[1]:
                    if current_time >= j[1] and current_time < j[2]:
                        if j != i[1][-1]:  # Accessing the next class available in the records
                            status = f"Next class:      {i[1][i[1].index(j) + 1][0]}\nStart time:      {i[1][i[1].index(j) + 1][1]}\nEnd time:        {i[1][i[1].index(j) + 1][2]}\n"
                            if button9['state'] == 'disabled':
                                button9['state'] = 'active'
                                status = "test"
                            return status
                        else:
                            status = "Phew, no other classes today!"
                            button9['state'] = 'disabled'
                            return status
                for k in i[1]:
                    if k[1] > current_time:
                        status = f"Next class:      {k[0]}\nStart time:      {k[1]}\nEnd time:        {k[2]}\n"
                        return status
                status = "Phew, no other classes today!"
                button9['state'] = 'disabled'
                return status
        status = "Phew, no other classes today!"
        button9['state'] = 'disabled'
        return status


def clock():  # Used to update label text every n seconds.
    message1.config(text=live_status())
    message1.after(1000, clock)


# Tool tip to display additional information
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)  # To show the tool tip when the cursor enters the widget
    widget.bind('<Leave>', leave)  # To stop showing the tool tip when the cursor moves away from the widget


def Join():
    global classes, data
    pickle_in = open(data, "rb")  # read the dat file for records
    classes = pickle.load(pickle_in)
    pickle_in.close()
    if len(classes) == 0:
        messagebox.showinfo("Invalid records", "Please fill the table using a valid template.")
        return
    else:
        button1['state'] = 'active'
        current_time = time.strftime("%H:%M:%S")
        for i in classes:
            if today == i[0]:
                for j in i[1]:
                    if current_time >= j[1] and current_time < j[2]:
                        webbrowser.open(j[3], new=2)  # new = 2 opens a new tab in the default browser (if possible)
                        return
                messagebox.showinfo("No class", "There's no class now, relax.")
                return
        messagebox.showinfo("No class", "There's no class now, relax.")
        return


def JoinNext():
    global classes, data
    pickle_in = open(data, "rb")  # read the dat file for records
    classes = pickle.load(pickle_in)
    pickle_in.close()
    if len(classes) == 0:
        button8['state'] = 'disabled'
        messagebox.showinfo("Invalid records", "Please fill the table using a valid template.")
        return
    else:
        current_time = time.strftime("%H:%M:%S")
        for i in classes:
            if today == i[0]:
                for j in i[1]:
                    if current_time >= j[1] and current_time < j[2]:
                        if i[1][i[1].index(j) + 1]:
                            webbrowser.open(i[1][i[1].index(j) + 1][3],
                                            new=2)  # new = 2 opens a new tab in the default browser (if possible)
                            return
                for k in i[1]:
                    if k[1] > current_time:
                        webbrowser.open(k[3], new=2)  # new = 2 opens a new tab in the default browser (if possible)
                        return
                messagebox.showinfo("Noo class", "There's no class now, relax.")
                return
        messagebox.showinfo("No class", "There's no class now, relax.")
        return


def addclass(event=None):
    global classes, url
    if combo1.get() == "--Select Day--":
        messagebox.showinfo("Invalid day", "Please select a valid day (Monday-Sunday)")
    else:
        if entry1.get() == "":
            messagebox.showinfo("Empty subject", "Please type a subject in the input field")
        else:
            if (entry2.get() == "hh:mm (24 hour format)" or entry2.get() == "" or len(entry2.get().split(":")) < 2
                or not entry2.get().split(":")[0].isdecimal() or not entry2.get().split(":")[1].isdecimal()
                or len(entry2.get().split(":")[1]) < 2 or int(entry2.get().split(":")[0]) < 0 or int(
                        entry2.get().split(":")[0]) > 24
                or int(entry2.get().split(":")[1]) < 0 or int(entry2.get().split(":")[1]) > 60) or (
                    entry3.get() == "hh:mm (24 hour format)"
                    or entry3.get() == "" or len(entry3.get().split(":")) < 2 or not entry3.get().split(":")[
                0].isdecimal()
                    or not entry3.get().split(":")[1].isdecimal() or len(entry3.get().split(":")[1]) < 2
                    or int(entry3.get().split(":")[0]) < 0 or int(entry3.get().split(":")[0]) > 24
                    or int(entry3.get().split(":")[1]) < 0 or int(entry3.get().split(":")[1]) > 60):
                messagebox.showinfo("Invalid time format", "Please type a 24 hour time format (hh:mm)")
            else:
                if int(entry2.get().split(":")[0]) < 10 and len(entry2.get().split(":")[0]) == 1:
                    entry2.insert(0, '0')
                if int(entry3.get().split(":")[0]) < 10 and len(entry3.get().split(":")[0]) == 1:
                    entry3.insert(0, '0')
                if int(entry2.get().split(":")[1]) < 10 and len(entry2.get().split(":")[1]) == 1:
                    entry2.insert(END, '0')
                if int(entry3.get().split(":")[1]) < 10 and len(entry3.get().split(":")[1]) == 1:
                    entry2.insert(END, '0')
                if entry2.get() > entry3.get():
                    messagebox.showinfo("Invalid value",
                                        "End time must be a time after start time. Imagine attending classes backwards.")
                else:
                    if "." not in entry4.get() or entry4.get() == "--valid url--":
                        messagebox.showinfo("Invalid URL", "Please enter a valid url (.com, .net, .org, etc.)")
                    else:
                        if not entry4.get().startswith('http'):
                            if entry4.get().startswith('www'):
                                url = "http://" + entry4.get()
                            else:
                                url = "http://www." + entry4.get()
                        else:
                            url = entry4.get()
                        for i in classes:
                            if i[0] == days.index(combo1.get()) - 1:
                                newdata = [entry1.get(), entry2.get(), entry3.get(), url]
                                if newdata not in i[1]:
                                    delete = open(data, "wb")  # clear existing data from the data file first
                                    pickle.dump([], delete)
                                    i[1].append(newdata)
                                    delete.close()
                                    pickle_out = open(data, "wb")
                                    pickle.dump(classes, pickle_out)
                                    pickle_out.close()
                                    fill_table()
                                    entry1.delete(0, END)
                                    entry2.delete(0, END)
                                    entry3.delete(0, END)
                                    entry4.delete(0, END)
                                    combo1.current(0)


def removeClass():
    global classes, data
    if tree1.selection() != ():
        if not any(i in ('0', '1', '2', '3', '4', '5', '6') for i in tree1.selection()):
            result = messagebox.askquestion("Delete Record",
                                            f"Are you sure you want to delete {len(tree1.selection())} record(s)?",
                                            icon='warning', default='no')
            if result == 'yes':
                for record in tree1.selection():
                    values = tree1.item(record)['values']
                    for i in classes:
                        if i[0] == int(tree1.parent(record)):
                            for j in i[1]:
                                if j[0] == values[0] and j[1] == values[1] and j[2] == values[2] and j[3] == values[3]:
                                    j.clear()
                                    i[1] = [x for x in i[1] if
                                            x]  # replaces i[1] after removing all empty sub lists in i[1]
                                    tree1.delete(record)
                                    break
                            break
                delete = open(data, "wb")  # clear existing data from the data file first
                pickle.dump([], delete)
                delete.close()
                pickle_out = open(data, "wb")
                pickle.dump(classes, pickle_out)
                pickle_out.close()
                fill_table()
        else:
            messagebox.showinfo("Unable to delete", "Make sure you're only selecting classes and not the day headings.")
    else:
        messagebox.showinfo("No record selected",
                            "Please select a record that you want to delete. (Can't delete emptiness)")


def removeAll():
    global classes, data
    result = messagebox.askquestion("Clear Table",
                                    "Are you sure you want to delete the entire table? (There's no undo though)",
                                    icon='warning', default='no')
    if result == 'yes':
        for record in tree1.get_children():
            for child in tree1.get_children(record):  # Get sub children
                values = tree1.item(child)['values']
                for i in classes:
                    if i[0] == int(record):
                        for j in i[1]:
                            if j[0] == values[0] and j[1] == values[1] and j[2] == values[2] and j[3] == values[3]:
                                j.clear()
                                i[1] = [x for x in i[1] if
                                        x]  # replaces i[1] after removing all empty sub lists in i[1]
                                tree1.delete(child)
                                break
                        break
            delete = open(data, "wb")  # clear existing data from the data file first
            pickle.dump([], delete)
            delete.close()
            pickle_out = open(data, "wb")
            pickle.dump(classes, pickle_out)
            pickle_out.close()
            fill_table()


def editClass():
    global record_no
    if len(tree1.selection()) != 0:
        if not any(i in ('0', '1', '2', '3', '4', '5', '6') for i in tree1.selection()):
            record_no = tree1.selection()[0]
            values = tree1.item(tree1.selection()[0])['values']
            combo1.current(int(tree1.parent(tree1.selection()[0])) + 1)
            entry1.delete(0, END)
            entry1.insert(0, values[0])
            entry2.delete(0, END)
            entry2.insert(0, values[1])
            entry3.delete(0, END)
            entry3.insert(0, values[2])
            entry4.delete(0, END)
            entry4.insert(0, values[3])
            button8["state"] = "active"
        else:
            messagebox.showinfo("Unable to delete", "Make sure you're only selecting classes and not the day headings.")
    else:
        messagebox.showinfo("No record selected", "Please select a class that you want to update.")


# Button9
img15 = PhotoImage(file="images/JoinNowButton.png")  # add "/" not "\"
button9 = Button(frame6, image=img15, command=JoinNext, borderwidth=0, bg="#2B2B26", relief=FLAT)
button9.grid(sticky=N + E + W + S)
button9.grid_rowconfigure(0, weight=100)
button9.grid_columnconfigure(0, weight=100)
button9.place(relx=0.25, rely=0.7)


def updateClass():
    global classes, record_no, data
    if tree1.selection() != ():
        if ('0' or '1' or '2' or '3' or '4' or '5' or '6') not in tree1.selection():
            values = tree1.item(record_no)['values']
            for i in classes:
                if i[0] == int(tree1.parent(record_no)):
                    for j in i[1]:
                        if j[0] == values[0] and j[1] == values[1] and j[2] == values[2] and j[3] == values[3]:
                            j.clear()
                            i[1] = [x for x in i[1] if
                                    x]  # replaces i[1] after removing all empty sub lists in i[1]
                            addclass()
                            tree1.delete(record_no)
                            break
                    break
            delete = open(data, "wb")  # clear existing data from the data file first
            pickle.dump([], delete)
            delete.close()
            pickle_out = open(data, "wb")
            pickle.dump(classes, pickle_out)
            pickle_out.close()
            fill_table()
        else:
            messagebox.showinfo("Unable to update", "Make sure you're only selecting classes and not the day headings.")
    else:
        messagebox.showinfo("No record selected", "Please select a record that you want to update.")
    button8['state'] = 'disabled'


def all_clear():
    combo1.current(0)
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry2.insert(0, "hh:mm (24 hour format)")
    entry3.delete(0, END)
    entry3.insert(0, "hh:mm (24 hour format)")
    entry4.delete(0, END)
    entry4.insert(0, "--valid url--")


# Save settings onto settings.dat
cb1 = tk.IntVar()
cb2 = tk.IntVar()


def savesettings():
    global settings
    system_out = open("data/settings.dat", "wb")  # Change the value in the DAT file
    settings['prompt'] = cb1.get()  # Update prompt setting
    settings['day'] = combo2.current()  # Update first day of the week setting
    settings['notifications'] = cb2.get()  # Update notifications setting
    pickle.dump(settings, system_out)
    system_out.close()

    # Label15
    label15 = Label(frame8, bg="black", fg="yellow", text="Settings saved.", font=('Verdana', 11, 'italic'))
    label15.grid(sticky=N + E + W + S, pady=0, padx=0)
    label15.grid_columnconfigure(0, weight=100)
    label15.grid_rowconfigure(0, weight=100)
    label15.place(relx=0.875, rely=0.9)
    frame8.update_idletasks()
    frame8.after(2000, label15.place_forget())


# Message1
message1 = Message(frame1, text="", font=('Verdana', 15), borderwidth=2, bg="black", fg="yellow", justify="left",
                   aspect=int(root.winfo_screenwidth() / 2))
message1.grid(sticky=N + E + W + S)
message1.grid_rowconfigure(0, weight=100)
message1.grid_columnconfigure(0, weight=100)
message1.place(relx=0.4, rely=0.55)

# Message2
message2 = Message(frame6, bg="#2B2B26", fg="yellow", text="", relief=FLAT, justify="left", font=('Verdana', 11),
                   aspect=int(frame6.winfo_screenwidth() - 20))
message2.grid(sticky=N + E + W + S)
message2.grid_rowconfigure(0, weight=100)
message2.grid_columnconfigure(0, weight=100)
message2.place(relx=0.08, rely=0.2)
clock()  # Call the function clock which recursively calls itself every second.

# Button1
img = PhotoImage(file="images/JoinButton.png")  # add "/" not "\"
button1 = Button(frame1, image=img, command=Join, borderwidth=0, bg="black", relief=FLAT)
button1.grid(sticky=N + E + W + S)
button1.grid_rowconfigure(0, weight=100)
button1.grid_columnconfigure(0, weight=100)
button1.place(relx=0.455, rely=0.68)

# Button2
img2 = PhotoImage(file="images/NewClassButton.png")  # add "/" not "\"
button2 = Button(frame2, image=img2, command=addclass, borderwidth=0, bg="black", relief=FLAT)
button2.grid(sticky=N + E + W + S)
button2.grid_rowconfigure(0, weight=100)
button2.grid_columnconfigure(0, weight=100)
button2.place(relx=0.84, rely=0.335)

# Button3
img9 = PhotoImage(file="images/ClearButton.png")
button3 = Button(frame2, image=img9, command=all_clear, borderwidth=0, bg="black", relief=FLAT)
button3.grid(sticky=N + E + W + S)
button3.grid_rowconfigure(0, weight=100)
button3.grid_columnconfigure(0, weight=100)
button3.place(relx=0.8, rely=0.12)

# Button4
img10 = PhotoImage(file="images/RemoveSelectedClassesButton.png")  # add "/" not "\"
button4 = Button(frame2, image=img10, command=removeClass, borderwidth=0, bg="black", relief=FLAT)
button4.grid(sticky=N + E + W + S)
button4.grid_rowconfigure(0, weight=100)
button4.grid_columnconfigure(0, weight=100)
button4.place(relx=0.05, rely=0.92)
CreateToolTip(button4, "Hold the control button and select the records you want to delete")

# Button5
img11 = PhotoImage(file="images/RemoveAllClassesButton.png")  # add "/" not "\"
button5 = Button(frame2, image=img11, command=removeAll, borderwidth=0, bg="black", relief=FLAT)
button5.grid(sticky=N + E + W + S)
button5.grid_rowconfigure(0, weight=100)
button5.grid_columnconfigure(0, weight=100)
button5.place(relx=0.835, rely=0.92)
CreateToolTip(button5, "Clear the table")

# Button6
img12 = PhotoImage(file="images/EditButton.png")  # add "/" not "\"
button6 = Button(frame2, image=img12, command=editClass, borderwidth=0, bg="black", relief=FLAT)
button6.grid(sticky=N + E + W + S)
button6.grid_rowconfigure(0, weight=100)
button6.grid_columnconfigure(0, weight=100)
button6.place(relx=0.05, rely=0.85)
CreateToolTip(button6, "Select a class and make changes")

# Button8
img13 = PhotoImage(file="images/UpdateClassButton.png")  # add "/" not "\"
button8 = Button(frame2, image=img13, command=updateClass, borderwidth=0, bg="black", relief=FLAT)
button8.grid(sticky=N + E + W + S)
button8.grid_rowconfigure(0, weight=100)
button8.grid_columnconfigure(0, weight=100)
button8.place(relx=0.845, rely=0.25)
button8['state'] = 'disabled'

# Button10
img19 = PhotoImage(file="images/CheckForUpdatesButton.png")  # add "/" not "\"
button10 = Button(frame7, image=img19, command=lambda: check_updates(1), bg="black", relief=FLAT)
button10.grid(sticky=N + E + W + S)
button10.grid_rowconfigure(0, weight=100)
button10.grid_columnconfigure(0, weight=100)
button10.place(relx=0.42, rely=0.6)

# Button11
img24 = PhotoImage(file="images/savebutton.png")  # add "/" not "\"
button11 = Button(frame8, image=img24, command=savesettings, bg="black", relief=FLAT)
button11.grid(sticky=N + E + W + S)
button11.grid_rowconfigure(0, weight=100)
button11.grid_columnconfigure(0, weight=100)
button11.place(relx=0.45, rely=0.9)


# Combo1
days = [
    "--Select Day--",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

style.map('TCombobox', fieldbackground=[('readonly', 'green')])
style.map('TCombobox', selectbackground=[('readonly', 'blue')])
style.map('TCombobox', selectforeground=[('readonly', 'red')])

logo = Image.open("images/OCH_Logo.png")
logo = logo.resize((180, 200), Image.ANTIALIAS)
img16 = ImageTk.PhotoImage(logo)
label9 = Label(frame1, image=img16, borderwidth=0, bg="black")
label9.grid(sticky=N + E + W + S, pady=0, padx=0)
label9.grid_columnconfigure(0, weight=100)
label9.grid_rowconfigure(0, weight=100)
label9.place(relx=0.438, rely=0.03)

logo2 = Image.open("images/OCH_Logo2.png")
logo2 = logo2.resize((100, 98), Image.ANTIALIAS)
img17 = ImageTk.PhotoImage(logo2)
label10 = Label(frame2, image=img17, borderwidth=0, bg="black")
label10.grid(sticky=N + E + W + S, pady=0, padx=0)
label10.grid_columnconfigure(0, weight=100)
label10.grid_rowconfigure(0, weight=100)
label10.place(relx=0.87, rely=0.07)

logo4 = Image.open("images/OCH_Logo.png")
logo4 = logo4.resize((200, 220), Image.ANTIALIAS)
img20 = ImageTk.PhotoImage(logo4)
label11 = Label(frame7, image=img20, borderwidth=0, bg="black")
label11.grid(sticky=N + E + W + S, pady=0, padx=0)
label11.grid_columnconfigure(0, weight=100)
label11.grid_rowconfigure(0, weight=100)
label11.place(relx=0.438, rely=0.15)

label12 = Label(frame7, text=f"Version {__version__}", font=('Times New Roman', 18), borderwidth=0, bg="black",
                fg="yellow")
label12.grid(sticky=N + E + W + S)
label12.grid_rowconfigure(0, weight=100)
label12.grid_columnconfigure(0, weight=100)
label12.place(relheight=0.05, relwidth=0.1, relx=0.448, rely=0.5)

# Label Frame (Add Class)
labelframe1 = LabelFrame(frame2, bg="black", font=("Helvetica", 12), foreground="yellow", text="Add Class")
labelframe1.grid(sticky=N + E + W + S)
labelframe1.place(relwidth=0.75, relheight=0.25, relx=0.05, rely=0.13)

# Label Frame (Settings)
labelframe2 = LabelFrame(frame8, bg="black", font=("Helvetica", 12), foreground="yellow", text="Settings")
labelframe2.grid(sticky=N + E + W + S)
labelframe2.place(relwidth=0.9, relheight=0.75, relx=0.05, rely=0.13)

# Label1
img4 = PhotoImage(file="images/ChooseDayLabel.png")
label1 = Label(labelframe1, bg="black", image=img4, command=None, relief=FLAT)
label1.grid(sticky=N + E + W + S)
label1.grid_rowconfigure(0, weight=100)
label1.grid_columnconfigure(0, weight=100)
label1.place(relx=0.02, rely=0.18)

# Label2
img5 = PhotoImage(file="images/EnterSubjectLabel.png")
label2 = Label(labelframe1, bg="black", image=img5, command=None, relief=FLAT)
label2.grid(sticky=N + E + W + S)
label2.grid_rowconfigure(0, weight=100)
label2.grid_columnconfigure(0, weight=100)
label2.place(relx=0.02, rely=0.61)

# Label3
img6 = PhotoImage(file="images/StartTimeLabel.png")
label3 = Label(labelframe1, bg="black", image=img6, command=None, relief=FLAT)
label3.grid(sticky=N + E + W + S)
label3.grid_rowconfigure(0, weight=100)
label3.grid_columnconfigure(0, weight=100)
label3.place(relx=0.36, rely=0.18)

# CheckButton1
img21 = PhotoImage(file="images/promptbutton.png")  # add "/" not "\"
checkbutton1 = Checkbutton(labelframe2, bg="black", image=img21, relief=FLAT, variable=cb1)
if settings['prompt']:
    checkbutton1.select()
else:
    checkbutton1.deselect()
checkbutton1.grid(sticky=N + E + W + S)
checkbutton1.grid_rowconfigure(0, weight=100)
checkbutton1.grid_columnconfigure(0, weight=100)
checkbutton1.place(relx=0.02, rely=0.1)

# Label14
img22 = PhotoImage(file="images/daylabel.png")  # add "/" not "\"
label14 = Label(labelframe2, bg="black", image=img22, relief=FLAT, highlightcolor='yellow')
label14.grid(sticky=N + E + W + S)
label14.grid_rowconfigure(0, weight=100)
label14.grid_columnconfigure(0, weight=100)
label14.place(relx=0.035, rely=0.3)

# Combo2 - Drop down menu
combo2 = ttk.Combobox(labelframe2, value=days, state="readonly", style="TCombobox")
combo2.current(settings['day'])
combo2.bind("<<ComboboxSelected>>", None)
combo2.grid(sticky=N + E + W + S)
combo2.grid_rowconfigure(0, weight=100)
combo2.grid_columnconfigure(0, weight=100)
combo2.place(relx=0.05, rely=0.4, relwidth=0.165)

# CheckButton2
img23 = PhotoImage(file="images/notificationbutton.png")  # add "/" not "\"
checkbutton2 = Checkbutton(labelframe2, bg="black", image=img23, relief=FLAT, variable=cb2)
if settings['notifications']:
    checkbutton2.select()
else:
    checkbutton2.deselect()
checkbutton2.grid(sticky=N + E + W + S)
checkbutton2.grid_rowconfigure(0, weight=100)
checkbutton2.grid_columnconfigure(0, weight=100)
checkbutton2.place(relx=0.35, rely=0.1)

# Label4
img7 = PhotoImage(file="images/EndTimeLabel.png")
label4 = Label(labelframe1, bg="black", image=img7, command=None, relief=FLAT)
label4.grid(sticky=N + E + W + S)
label4.grid_rowconfigure(0, weight=100)
label4.grid_columnconfigure(0, weight=100)
label4.place(relx=0.36, rely=0.61)

# Label5
img8 = PhotoImage(file="images/ClassLinkLabel.png")
label5 = Label(labelframe1, bg="black", image=img8, command=None, relief=FLAT)
label5.grid(sticky=N + E + W + S)
label5.grid_rowconfigure(0, weight=100)
label5.grid_columnconfigure(0, weight=100)
label5.place(relx=0.67, rely=0.18)

# Label6
abouttext = '''Copyright (C) Ravens Enterprises - All Rights Reserved
* Unauthorized copying of this file, via any medium is strictly prohibited
* Open-source (Source code will be available on Github and Sourceforge)
* Written by Rahul Maddula, July 2021

OCH is a free-of-cost open source software which is designed with an intention to try and help as many students
attending online classes as possible in the current pandemic.

OCH was designed using Python programming language and was released in July 2021.

About the Author
--------------------
OCH was designed and programmed by Rahul Maddula
You can interact or contact me for any information through my email and social media handles given on Help>>Contact'''

label6 = Label(frame3, text=abouttext, font=('Times New Roman', 18), borderwidth=0, bg="black", fg="yellow")
label6.grid(sticky=N + E + W + S)
label6.grid_rowconfigure(0, weight=100)
label6.grid_columnconfigure(0, weight=100)
label6.place(relheight=1.3, relwidth=1)

logo3 = Image.open("images/OCH_Logo2.png")
logo3 = logo3.resize((200, 196), Image.ANTIALIAS)
img18 = ImageTk.PhotoImage(logo3)
label8 = Label(frame3, image=img18, borderwidth=0, bg="black")
label8.grid(sticky=N + E + W + S, pady=0, padx=0)
label8.grid_columnconfigure(0, weight=100)
label8.grid_rowconfigure(0, weight=100)
label8.place(relx=0.438, rely=0.075)

# Label7
helptext = '''For any kind of bugs/issues/help/details please contact the owner through the following:
Personal Email: vensr.maddula@gmail.com
Business Email: ravensenterprises8@gmail.com
Personal Instagram handle: @vens8
Personal Twitter handle: @vens_8
'''

label7 = Label(frame4, text=helptext, font=('Times New Roman', 18), borderwidth=0, bg="black", fg="yellow")
label7.grid(sticky=N + E + W + S)
label7.grid_rowconfigure(0, weight=100)
label7.grid_columnconfigure(0, weight=100)
label7.place(relheight=1, relwidth=1)

# Combo1 - Drop down menu
combo1 = ttk.Combobox(labelframe1, value=days, state="readonly", style="TCombobox")
combo1.current(0)
combo1.bind("<<ComboboxSelected>>", None)
combo1.grid(sticky=N + E + W + S)
combo1.grid_rowconfigure(0, weight=100)
combo1.grid_columnconfigure(0, weight=100)
combo1.place(relx=0.165, rely=0.2, relwidth=0.165)


def e2_clear(event):
    if entry2.get() == "hh:mm (24 hour format)":
        entry2.delete(0, "end")


def e3_clear(event):
    if entry3.get() == "hh:mm (24 hour format)":
        entry3.delete(0, "end")


def e4_clear(event):
    if entry4.get() == "--valid url--":
        entry4.delete(0, "end")


# Entry1
entry1 = Entry(labelframe1, fg="yellow", bg="black", highlightcolor="green", highlightthickness=0.5, justify="left",
               font=("Helvetica", 10), insertbackground='yellow')
entry1.grid(sticky=N + E + W + S)
entry1.grid_rowconfigure(0, weight=100)
entry1.grid_columnconfigure(0, weight=100)
entry1.place(relx=0.165, rely=0.64, relwidth=0.165)

# Entry2
entry2 = Entry(labelframe1, fg="yellow", bg="black", highlightcolor="green", highlightthickness=0.5, justify="left",
               font=("Helvetica", 10), insertbackground='yellow')
entry2.insert(0, "hh:mm (24 hour format)")
entry2.grid(sticky=N + E + W + S)
entry2.grid_rowconfigure(0, weight=100)
entry2.grid_columnconfigure(0, weight=100)
entry2.bind("<FocusIn>", e2_clear)
entry2.place(relx=0.48, rely=0.21, relwidth=0.165)

# Entry3
entry3 = Entry(labelframe1, fg="yellow", bg="black", highlightcolor="green", highlightthickness=0.5, justify="left",
               font=("Helvetica", 10), insertbackground='yellow')
entry3.insert(0, "hh:mm (24 hour format)")
entry3.grid(sticky=N + E + W + S)
entry3.grid_rowconfigure(0, weight=100)
entry3.grid_columnconfigure(0, weight=100)
entry3.bind("<FocusIn>", e3_clear)
entry3.place(relx=0.48, rely=0.64, relwidth=0.165)

# Entry4
entry4 = Entry(labelframe1, fg="yellow", bg="black", highlightcolor="green", highlightthickness=0.5, justify="left",
               font=("Helvetica", 10), width=40, insertbackground='yellow')
entry4.insert(0, "--valid url--")
entry4.grid(sticky=N + E + W + S)
entry4.grid_rowconfigure(0, weight=100)
entry4.grid_columnconfigure(0, weight=100)
entry4.bind("<FocusIn>", e4_clear)
entry4.place(relx=0.79, rely=0.21, relwidth=0.2)

# Tree view frame
frame5 = tk.Frame(frame2, bg="black")
frame5.grid(sticky=N + E + W + S, row=0, column=0, pady=0, padx=0)
frame5.grid_rowconfigure(0, weight=1)
frame5.grid_columnconfigure(0, weight=1)
frame5.place(relx=0.05, rely=0.42, relwidth=0.96, relheight=0.4)

frames = [frame1,
          frame2,
          frame3,
          frame4,
          frame5,
          frame6,
          frame7,
          frame8,
          frame9
          ]

# Scrollbar
scrollbar1 = ttk.Scrollbar(frame5, orient=VERTICAL)
scrollbar1.grid(sticky=N + S + E + W, row=0, column=1)
scrollbar1.grid_rowconfigure(0, weight=1)
scrollbar1.grid_columnconfigure(0, weight=1)

# Tree view table
tree1 = ttk.Treeview(frame5, yscrollcommand=scrollbar1.set)
tree1['columns'] = ("Day", "Start time", "End time", "Class link")
tree1.column("#0", width=0, anchor=W)
tree1.column("Day", anchor=W, width=100)
tree1.column("Start time", anchor=W, width=50)
tree1.column("End time", anchor=W, width=50)
tree1.column("Class link", anchor=W, width=700)
tree1.heading("#0", text="", anchor=W)
tree1.heading("Day", text="Day : Subject", anchor=W)
tree1.heading("Start time", text="Start time", anchor=W)
tree1.heading("End time", text="End time", anchor=W)
tree1.heading("Class link", text="Class link", anchor=W)
scrollbar1.config(command=tree1.yview)
style.theme_use("clam")
style.configure("Treeview.Heading",
                font=("Helvetica", 12, "bold"),
                background="#581845",
                foreground="white",
                relief="flat",
                )
style.configure("Treeview",
                font=("Helvetica", 11),
                background="#FFC30F",
                foreground="#FFFF00",
                rowheight=45,
                fieldbackground="black"
                )
style.configure("Vertical.TScrollbar", background="#581845", darkcolor="#FFC30F", lightcolor="#FFC30F",
                troughcolor="#B28500", bordercolor="black", arrowcolor="white"
                )
style.map("Treeview",
          background=[("selected", "#FFC30F")],
          foreground=[("selected", "black")]
          )
tree1.tag_configure('even', background="#C70039", font=("Helvetica", 11, 'bold'))
tree1.tag_configure('odd', background="#A50240", font=("Helvetica", 11, 'bold'))
tree1.tag_configure('child', background="#FF5733")


# Table data
def fill_table():
    global classes
    sortRecords()
    for i in tree1.get_children():  # Clear table
        tree1.delete(i)
    id_count = 0
    c_count = 0
    for i in classes:
        if id_count % 2 == 0:
            tree1.insert(parent='', index="end", iid=id_count, open=True, text="", values=(days[i[0] + 1], "", "", ""),
                         tags=('even',))
            id_count += 1
        else:
            tree1.insert(parent='', index="end", iid=id_count, open=True, text="", values=(days[i[0] + 1], "", "", ""),
                         tags=('odd',))
            id_count += 1
        if id_count > 0:
            sep = ttk.Separator(tree1, orient='horizontal')
            sep.grid(sticky="news")
    for i in classes:
        for j in i[1]:
            if c_count < id_count:
                tree1.insert(parent=f"{c_count}", index="end", iid=id_count, open=False, text="",
                             values=(j[0], j[1], j[2], j[3]), tags=('child',))
                id_count += 1
            else:
                break
        c_count += 1
        if c_count >= id_count:
            break


fill_table()
tree1.grid(pady=20, padx=20)
tree1.place(relx=0, rely=0, relwidth=0.937, relheight=1)

# Button 7
img3 = PhotoImage(file="images/LoadDataButton.png")
button7 = Button(frame2, image=img3, command=load_file, borderwidth=0, bg="black", relief=RIDGE)
button7.grid(sticky=N + E + W + S)
button7.grid_rowconfigure(0, weight=100)
button7.grid_columnconfigure(0, weight=100)
button7.place(relx=0.875, rely=0.85)

root.mainloop()
