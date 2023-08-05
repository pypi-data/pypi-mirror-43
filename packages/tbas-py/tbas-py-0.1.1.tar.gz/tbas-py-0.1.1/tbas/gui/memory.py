from tkinter import *
from tbas.gui.cell import Cell
from tbas.datatypes import Memory
from typing import List
from functools import partial


class Mem:

    def __init__(self, master, size=32, title=""):
        self.cells: List[Cell] = []
        self.last_highlight = None
        self.update_callback = lambda a,b: None

        frame = LabelFrame(master, text=title)
        frame.pack(side=TOP, anchor=W, padx=2, fill=X)

        # pinched from https://stackoverflow.com/a/16198198
        scroll_bar = Scrollbar(frame, orient=HORIZONTAL)
        scroll_bar.pack(fill=X, side=BOTTOM, expand=FALSE)
        canvas = Canvas(frame, bd=0, highlightthickness=0, height=100,
                        xscrollcommand=scroll_bar.set)
        canvas.pack(side=BOTTOM, fill=BOTH, expand=TRUE)
        scroll_bar.config(command=canvas.xview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)


        # buttonFrame = Frame(interior)
        # buttonFrame.pack(side=TOP, anchor=NW)
        # v = IntVar()
        # v.set(Mode.INT)
        #
        # Radiobutton(buttonFrame, text="HEX", command=partial(self.change_mode, Mode.HEX), variable=v, value=Mode.HEX).pack(side=LEFT)
        # intbutton = Radiobutton(buttonFrame, text="INT", command=partial(self.change_mode, Mode.INT), variable=v, value=Mode.INT)
        # intbutton.select()
        # intbutton.pack(side=LEFT)
        # Radiobutton(buttonFrame, text="CHR", command=partial(self.change_mode, Mode.CHR), variable=v, value=Mode.CHR).pack(side=LEFT)

        for i in range(size):
            self.cells.append(Cell(self.interior, index=i))
    #
    # def change_mode(self, new_mode):
    #     print("Setting mode to ", new_mode)
    #     for cell in self.cells:
    #         cell.set_mode(new_mode)

    def update(self, new_vals: Memory):
        for index, cell in enumerate(self.cells):
            if index in range(len(new_vals)):
                cell.set_val(new_vals[index])
                cell.update_callback = partial(self.update_callback, index)
            else:
                cell.set_val(0)

    def reset(self):
        for cell in self.cells:
            cell.highlight(None)
        self.last_highlight = None

    def highlight(self, index):
        if self.last_highlight is not None:
            self.cells[self.last_highlight].highlight(None)
        if index not in range(len(self.cells)):
            return
        self.cells[index].highlight("red")
        self.last_highlight = index
