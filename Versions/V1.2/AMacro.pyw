import time
import threading
import tkinter as tk
import pyautogui as pg
from ctypes import windll
from PIL import Image, ImageTk

windll.shcore.SetProcessDpiAwareness(1)

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
    def __init__(self, size=(20, 20), link=None, **options):
        # imgChecked = Image.open(r'D:\Tkinter\AMacro\checked.png').resize(size, Image.ANTIALIAS)
        # imgUnchecked = Image.open(r'D:\Tkinter\AMacro\unchecked.png').resize(size, Image.ANTIALIAS)
        imgChecked = Image.open(r'.\extras\checked.png').resize(size, Image.ANTIALIAS)
        imgUnchecked = Image.open(r'.\extras\unchecked.png').resize(size, Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(imgChecked)
        self.img2 = ImageTk.PhotoImage(imgUnchecked)
        self.cBox = tk.Button(image=self.img2, command=self.switch, **options)
        self.state = 0
        self.link = link

    def place(self, **options):
        self.cBox.place(**options)

    def grid(self, **options):
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
    def __init__(self, master, row):
        self.cbox = Checkbox(master=master, link=self, **cboxStyle)
        self.ent_command = tk.Entry(master, **entryStyle)
        self.lbl_multiplier = tk.Label(master, text='X', **labelStyle)
        self.ent_multiplier = tk.Entry(master, width=5, **entryStyle)
        self.ent_multiplier.insert(0, 1)
        self.btn_clear = tk.Button(master, text=' X ', command=self.clear, **smlbuttonStyle)

        self.cbox.grid(column=0, row=row)
        self.ent_command.grid(column=1, row=row, sticky='nsew')
        self.lbl_multiplier.grid(column=2, row=row)
        self.ent_multiplier.grid(column=3, row=row)
        self.btn_clear.grid(column=4, row=row)

    def clear(self):
        self.cbox.off()
        self.ent_command.delete(0, tk.END)
        self.ent_multiplier.delete(0, tk.END)
        self.ent_multiplier.insert(0, 1)


def output(text):
    global txt_output

    txt_output.insert(tk.END, text + '\n')


def entry():
    global rowObj
    global ent_iter
    global ent_sleep
    global root
    global masterBreak
    masterBreak = 0

    collection = {}
    command = {}

    try:
        for obj in rowObj:
            if obj.cbox.state == 1:
                command[obj.ent_command.get()] = int(obj.ent_multiplier.get())
        collection['iter'] = int(ent_iter.get())
        collection['sleep'] = float(ent_sleep.get())

        output('Output Started.')
        time.sleep(4)
        for iter in range(collection['iter']):
            for entry in command:
                for _ in range(command[entry]):
                    if masterBreak == 1:
                        output('---stopped---')
                        return
                    pg.typewrite(entry, interval=0.2)
                    pg.press(['return'])
                    time.sleep(collection['sleep'])
        output('---end---')

    except Exception:
        output('---stopped---')


def run():
    runThread = threading.Thread(target=entry)
    runThread.start()


def reset():
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


def stop():
    global masterBreak
    masterBreak = 1


root = tk.Tk()
root.title('AMacro V1.2')
# root.geometry('419x400')
root.configure(**frameStyle)
masterBreak = 0

root.columnconfigure([0, 2, 4], minsize=40)
root.columnconfigure(1, minsize=90)
root.columnconfigure(3, minsize=50)

lbl_command = tk.Label(text='Command', **labelStyle)
lbl_command.grid(column=1, row=0)

lbl_multiplier = tk.Label(root, text='Multiplier', **labelStyle)
lbl_multiplier.grid(column=3, row=0)

lbl_clear = tk.Label(root, text='Clear', **labelStyle)
lbl_clear.grid(column=4, row=0, sticky='n')

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
txt_output.grid(column=0, row=end + 6, columnspan=5, sticky='nsew')

root.mainloop()
