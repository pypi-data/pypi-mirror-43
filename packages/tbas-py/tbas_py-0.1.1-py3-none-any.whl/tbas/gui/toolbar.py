from tkinter import *


class ToolBar():

    def __init__(self, master, run_callback, continue_callback, step_callback, reset_callback):
        frame = Frame(master, bd=0)
        frame.pack(side=TOP, anchor=N, pady=2)

        # self._run_icon = PhotoImage(file="gui/icons/run.gif")
        # self._reset_icon = PhotoImage(file="gui/icons/reset.gif")
        # self._continue_icon = PhotoImage(file="gui/icons/continue.gif")
        # self._step_icon = PhotoImage(file="gui/icons/step.gif")

        self.run_button = Button(frame, command=run_callback, text="RUN", width=10, height=3, justify=CENTER)#, image=self._run_icon)
        self.run_button.pack(side=LEFT, padx=10)

        self.continue_button = Button(frame, command=continue_callback, text="CONTINUE", width=10, height=3, justify=CENTER)#, image=self._continue_icon)
        self.continue_button.pack(side=LEFT, padx=10)

        self.step_button = Button(frame, command=step_callback, text="STEP", width=10, height=3, justify=CENTER)#, image=self._step_icon)
        self.step_button.pack(side=LEFT, padx=10)

        self.reset_button = Button(frame, command=reset_callback, text="RESET", width=10, height=3, justify=CENTER)#, image=self._reset_icon)
        self.reset_button.pack(side=LEFT, padx=10)
