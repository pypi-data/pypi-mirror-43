from tkinter import *


class StatusBar():

    def __init__(self, master):
        frame = Frame(master, bd=0)
        frame.pack(side=BOTTOM, anchor=W, fill=X, padx=2)

        self.label = Label(frame, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
