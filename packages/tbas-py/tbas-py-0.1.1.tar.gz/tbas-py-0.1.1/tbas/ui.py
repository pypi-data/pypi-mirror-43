from tkinter import Tk
from tbas.machine import Machine
from tbas.gui.memory import Mem
from tbas.gui.program import Program
from tbas.gui.status import StatusBar
from tbas.gui.toolbar import ToolBar


class UI:

    def __init__(self, machine: Machine = Machine(program="+++[?-]"), running=False):
        self.machine = machine
        self.running = running

        self.root = Tk()
        self.toolbar = ToolBar(self.root, self.run, self.continue_exec, self.step, self.reset)
        self.program = Program(self.root, machine.program)
        self.buffer = Mem(self.root, title="Buffer", size=machine.buffer.max_length)
        self.memory = Mem(self.root, title="Memory", size=machine.num_cells)
        self.status = StatusBar(self.root)

        self.buffer.update_callback = self.update_buf
        self.memory.update_callback = self.update_mem

        self.update()

    def update_mem(self, index, val):
        self.machine.memory[index] = val

    def update_buf(self, index, val):
        if index in range(len(self.machine.buffer.buffer)):
            self.machine.buffer.buffer[index] = val

    def run(self):
        self.continue_exec()

    def continue_exec(self, n=65536):
        timeout = n - 1
        self.running = True
        should_continue = self.machine.step_once()
        while should_continue and timeout > 0 and self.machine.ip not in self.program.breakpoints and self.running:
            try:
                should_continue = self.machine.step_once()
                self.update()
            except Exception as e:
                self.update()
                raise e
            timeout -= 1
        self.running = False

    def step(self):
        self.machine.step_once()
        self.update()

    def reset(self):
        self.running = False
        saved_program = self.machine.program
        self.machine.clean_init()
        self.machine.load_program(saved_program)

        self.program.reset()
        self.update()

    def update(self):
        self.status.set("Instruction Pointer: %d | Data Pointer %d | IO Mode %d",
                        self.machine.ip,
                        self.machine.data_pointer,
                        self.machine.io_mode)
        self.buffer.update(self.machine.buffer.buffer)
        self.memory.update(self.machine.memory)
        self.memory.highlight(self.machine.data_pointer)
        self.program.highlight(self.machine.ip)
        self.root.update()

    def _start(self):
        self.root.mainloop()
        if self.running:
            self.run()


def main():
    UI(machine=Machine(program=input("> ")))._start()


if __name__ == '__main__':
    main()
