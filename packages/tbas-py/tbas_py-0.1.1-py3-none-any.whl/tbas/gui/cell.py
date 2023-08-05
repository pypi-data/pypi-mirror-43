from tkinter import *
from enum import IntEnum


class Mode(IntEnum):
    INT = 1,
    HEX = 2,
    CHR = 3


class Cell:

    mode = Mode.INT

    def __init__(self, master, index=0):
        self.update_callback = lambda _: True

        self.master = master
        self.frame = Frame(master)
        self.frame.pack(side=LEFT)

        self._index = Label(self.frame, text=(str(index) if (index % 5 == 0) else ""), font='TkFixedFont')
        self._index.pack()

        self.contents = StringVar()
        intval = master.register(self.validation_dispatch)
        self._contents = Entry(self.frame, width=3, textvariable=self.contents,
                          justify=CENTER, validate="key",
                          vcmd=(intval, '%P'), font='TkFixedFont')
        self._contents.pack()

        self.int = IntVar()

        self.char = StringVar()
        self._char = Label(self.frame, width=3, textvariable=self.char, justify=CENTER, font='TkFixedFont')
        self._char.pack()

        self.contents.trace("w", self.update)
        self.set_val(0)


    def validation_dispatch(self, res):
        if res == "":
            return True
        if len(res) > 4:
            return False
        if self.mode == Mode.INT:
            return self.check_num_bounds(res)
        if self.mode == Mode.HEX:
            return self.check_num_bounds(res, base=16)
        if self.mode == Mode.CHR:
            return self.check_char_bounds(res)

    def check_num_bounds(self, res, base=10):
        try:
            i = int(res, base)
            if i < 0 or i > 255:
                raise ValueError("Out of valid byte bounds")
            return True
        except ValueError:
            return False

    def check_char_bounds(self, res):
        return len(res) == 1 and ord(res) < 256

    def update(self, *_args):
        val = self.contents.get()
        if self.mode == Mode.INT:
            self.int.set(int(val) if (val != "") else 0)
        if self.mode == Mode.HEX:
            self.int.set(int(val, 16) if (val != "") else 0)
        if self.mode == Mode.CHR:
            self.int.set(ord(val) if (val != "") else self.int.get())
        self.char.set(chr(self.int.get()) if self.int.get() > 31 else '_')
        self.update_callback(self.int.get())

    def set_mode(self, new_mode):
        self.mode = new_mode
        if self.mode == Mode.HEX:
            self.contents.set(format(self.int.get(), 'x'))
        if self.mode == Mode.CHR:
            self.contents.set(chr(self.int.get()))
        if self.mode == Mode.INT:
            self.contents.set(self.int.get())

    def set_val(self, new_value: int):
        if self.mode == Mode.INT:
            self.contents.set(str(new_value))
        if self.mode == Mode.HEX:
            self.contents.set(format(new_value, 'x'))
        if self.mode == Mode.CHR:
            self.contents.set(chr(new_value) if new_value > 31 else "")

    def highlight(self, color):
        if color is not None:
            self._contents.config(fg=color)
        else:
            self._contents.config(fg="black")
