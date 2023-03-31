import time
import threading
import tkinter as tk
import pyautogui as pg
from ctypes import windll
from PIL import Image, ImageTk

# Make the process DPI-aware for better scaling on high-DPI displays
windll.shcore.SetProcessDpiAwareness(1)

# styles for widgets
labelStyle = {
    'bg': '#2f2f2f',
    'fg': 'white',
    'font': '"Microsoft YaHei UI Light" 11'
}

entryStyle = {
    'bg': '#3f3f3f',
    'fg': 'white',
    'font': '"Microsoft YaHei UI Light" 11',
    'relief': 'flat',
    'highlightthickness': '1',
    'highlightcolor': '#06aef9',
    'highlightbackground': '#272727'
}

smlbuttonStyle = {
    'bg': '#3f3f3f',
    'fg': 'white',
    'font': '"Microsoft YaHei UI Light" 8',
    'relief': 'flat',
    'activebackground': '#272727',
    'activeforeground': '#06aef9',
    'borderwidth': '0'
}

buttonStyle = {
    'bg': '#3f3f3f',
    'fg': 'white',
    'font': '"Microsoft YaHei UI Light" 10',
    'relief': 'flat',
    'activebackground': '#272727',
    'activeforeground': '#06aef9',
    'borderwidth': '0'
}

cboxStyle = {
    'bg': '#2f2f2f',
    'relief': 'flat',
    'borderwidth': '0',
    'activebackground': '#2f2f2f',
}

frameStyle = {'bg': '#2f2f2f'}


class Checkbox:
    '''A checkbox widget with on/off state and link to a function'''

    def __init__(self, size=(20, 20), link=None, **options):
        '''sets up the checkbox with the given size and link to a function'''

        # load the images
        imgChecked = Image.open(r'.\extras\checked.png').resize(size, Image.ANTIALIAS)
        imgUnchecked = Image.open(r'.\extras\unchecked.png').resize(size, Image.ANTIALIAS)

        # create the images for the button and set the initial state
        self.img1 = ImageTk.PhotoImage(imgChecked)
        self.img2 = ImageTk.PhotoImage(imgUnchecked)
        self.cBox = tk.Button(image=self.img2, command=self.switch, **options)
        self.state = 0
        self.link = link

    def place(self, **options):
        '''places the checkbox on the screen and set options'''
        self.cBox.place(**options)

    def grid(self, **options):
        '''places the checkbox in grid and set options'''
        self.cBox.grid(**options)

    def switch(self):
        if self.state == 1:
            self.off()
        else:
            self.on()

    def on(self):
        self.cBox.configure(image=self.img1)
        self.state = 1

    def off(self):
        self.cBox.configure(image=self.img2)
        self.state = 0


class RowGen:
    '''A class to generate rows of widgets, this makes the row that contains all the input functionality'''

    def __init__(self, master, row):
        '''sets up the row with the given master and row number'''
        self.rowNo = row

        # create the widgets
        self.cbox = Checkbox(master=master, link=self, **cboxStyle)
        self.ent_command = tk.Entry(master, **entryStyle)
        self.lbl_multiplier = tk.Label(master, text='X', **labelStyle)
        self.ent_multiplier = tk.Entry(master, width=5, **entryStyle)
        self.ent_multiplier.insert(0, 1)
        self.ent_sTime = tk.Entry(master, width=5, **entryStyle)

        #sets specific time to 4 for the first row and clear button
        if row == 1:
            self.ent_sTime.insert(0, 4)
        else:
            self.ent_sTime.insert(0, '')
        self.btn_clear = tk.Button(master, text=' X ', command=self.clear, **smlbuttonStyle)

        # place all the widgets into a grid
        self.cbox.grid(column=0, row=row)
        self.ent_command.grid(column=1, row=row, sticky='nsew')
        self.lbl_multiplier.grid(column=2, row=row)
        self.ent_multiplier.grid(column=3, row=row)
        self.ent_sTime.grid(column=4, row=row)
        self.btn_clear.grid(column=5, row=row)

    def clear(self):
        '''clears the row and sets to initial state'''
        self.cbox.off()
        self.ent_command.delete(0, tk.END)
        self.ent_multiplier.delete(0, tk.END)
        self.ent_multiplier.insert(0, 1)


def output(text):
    '''outputs the given text to the output box(the bottom big box)'''
    global txt_output

    txt_output.insert(tk.END, text + '\n')


def entry():
    '''the main function that runs the program, collects the inputs from each row and performs the output function'''
    global rowObj
    global row1
    global ent_iter
    global ent_sleep
    global root
    global masterBreak
    masterBreak = 0

    # it contains the number of global iterations and sleep time
    collection = {}  # Collection {iter: int, sleep: float}

    # it contains the commands and their multiplier and specific time
    command = {}  # Command {command: [multiplier, sTime(of next row field)]}

    try:
        # collect the data from each row
        for index, obj in enumerate(rowObj):
            if obj.cbox.state == 1: #collects only if the checkbox is checked
                command[obj.ent_command.get()] = [int(obj.ent_multiplier.get()), ]
                if index + 1 < len(rowObj):
                    nxtRowObj = rowObj[index + 1]
                    if nxtRowObj.ent_sTime.get():
                        command[obj.ent_command.get()].append(float(nxtRowObj.ent_sTime.get()))
                    else:
                        command[obj.ent_command.get()].append(None)
                else:
                    command[obj.ent_command.get()].append(None)

        # collect the data from total iterations and sleep time
        collection['iter'] = int(ent_iter.get())
        collection['sleep'] = float(ent_sleep.get())

        output('Output Started.')

        # initial sleep time
        time.sleep(float(row1.ent_sTime.get()))

        # main loop; it collects the row data and outputs that data
        for iter in range(collection['iter']):  # To collect no of times
            for entry in command:  # For collecting command
                for _ in range(command[entry][0]):  # For multiplier
                    
                    # threading can stop the program
                    if masterBreak == 1:
                        output('---stopped---')
                        return
                    
                    pg.typewrite(entry, interval=0.01)
                    pg.press(['return'])
                    
                    if command[entry][1]:
                        time.sleep(command[entry][1])
                    else:
                        time.sleep(collection['sleep'])
       
        output('---end---')

    except Exception as e:
        output('---stopped---')
        print(e)


def run():
    '''runs the entry function in a thread'''
    runThread = threading.Thread(target=entry)
    runThread.start()


def reset():
    '''resets the program to initial state'''
    global rowObj
    global ent_iter
    global ent_sleep

    for obj in rowObj:
        obj.cbox.off()
        obj.ent_command.delete(0, tk.END)
        obj.ent_multiplier.delete(0, tk.END)
        obj.ent_multiplier.insert(0, 1)
        ent_iter.delete(0, tk.END)
        ent_iter.insert(0, 100)
        ent_sleep.delete(0, tk.END)
        ent_sleep.insert(0, 3)
        obj.ent_sTime.delete(0, tk.END)
        if obj.rowNo == 1:
            obj.ent_sTime.insert(0, 4)


def stop():
    '''stops the program'''
    global masterBreak
    masterBreak = 1

# set main window
root = tk.Tk()
root.title('AMacro V1.3')
# root.geometry('419x400')
root.configure(**frameStyle)
masterBreak = 0

#grid config for root
root.columnconfigure([0, 2, 5], minsize=40)
root.columnconfigure(1, minsize=90)
root.columnconfigure(3, minsize=50)
root.columnconfigure(4, minsize=60)


# top row labels
lbl_command = tk.Label(text='Command', **labelStyle)
lbl_command.grid(column=1, row=0)

lbl_multiplier = tk.Label(root, text='Multiplier', **labelStyle)
lbl_multiplier.grid(column=3, row=0)

lbl_specificTime = tk.Label(root, text='S. Time', **labelStyle)
lbl_specificTime.grid(column=4, row=0)

lbl_clear = tk.Label(root, text='Clear', **labelStyle)
lbl_clear.grid(column=5, row=0, sticky='n')

# row generator; should use a loop
row1 = RowGen(root, 1)
row2 = RowGen(root, 2)
row3 = RowGen(root, 3)
row4 = RowGen(root, 4)
row5 = RowGen(root, 5)
row6 = RowGen(root, 6)
row7 = RowGen(root, 7)
row8 = RowGen(root, 8)

rowObj = [row1, row2, row3, row4, row5, row6, row7, row8]

end = 8

# bottom row labels and boxes
lbl_empty = tk.Label(root, **labelStyle)
lbl_empty.grid(column=0, row=end + 1)

lbl_times = tk.Label(root, text='     No. of Times:', **labelStyle)
lbl_times.grid(column=1, row=end + 2, sticky='w')

ent_iter = tk.Entry(root, width=5, **entryStyle)
ent_iter.insert(0, '100')
ent_iter.grid(column=1, row=end + 2, sticky='e')

lbl_sleep = tk.Label(root, text='     SleepTime(sec):', **labelStyle)
lbl_sleep.grid(column=1, row=end + 3, sticky='w')

ent_sleep = tk.Entry(root, width=5, **entryStyle)
ent_sleep.insert(0, '3')
ent_sleep.grid(column=1, row=end + 3, sticky='e')

lbl_empty.grid(column=0, row=end + 4)

btn_run = tk.Button(root, text='Run', padx=15, command=run, **buttonStyle)
btn_run.grid(column=1, row=end + 5, sticky='e', padx=65)

btn_stop = tk.Button(root, text='Stop', padx=6, command=stop, **buttonStyle)
btn_stop.grid(column=1, row=end + 5, sticky='e')

btn_reset = tk.Button(root, text='Reset', command=reset, **buttonStyle)
btn_reset.grid(column=2, row=end + 5, sticky='w', columnspan=2, padx=10)

txt_output = tk.Text(root, width=25, height=6, **entryStyle)
txt_output.grid(column=0, row=end + 6, columnspan=6, sticky='nsew')

#run the main loop
root.mainloop()
