from string import ascii_lowercase, ascii_uppercase, digits
from typing import List
import sys

tbas_chars = ['+', '-', '<', '>', '[', ']', '=', '?']


def not_implemented(_machine):
    print("IO MODE NOT IMPLEMENTED")


def console_write(wr):
    sys.stdout.write(str(wr))
    sys.stdout.flush()


def buffer_program(m):
    m.buffer.clear()
    for k in m.program:
        m.buffer.enqueue(ord(k))


def set_mcell(m, newval: int):
    m.mcell = newval


def convert(index: int, lang: List[str]) -> int:
    if index not in range(0, len(lang)):
        return index
    return ord(lang[index])


io_modes = [
    lambda m: console_write(int(m.mcell)),  # 0
    lambda m: set_mcell(m, int(input('d> '))),
    lambda m: console_write(chr(m.mcell)),
    lambda m: set_mcell(m, ord(input('a> ')[0])),
    not_implemented,  # modem write
    not_implemented,  # modem read
    buffer_program,
    lambda m: m.execute_task(m.mcell),
    lambda m: m.buffer.enqueue(m.mcell),
    lambda m: set_mcell(m, m.buffer.dequeue_filo()),
    lambda m: set_mcell(m, m.buffer.dequeue_fifo()),  # 10
    lambda m: m.buffer.clear(),
    lambda m: set_mcell(m, convert(m.mcell, ascii_lowercase)),
    lambda m: set_mcell(m, convert(m.mcell, ascii_uppercase)),
    lambda m: set_mcell(m, convert(m.mcell, digits)),
    lambda m: set_mcell(m, convert(m.mcell, tbas_chars)),  # 15
    lambda m: set_mcell(m, m.mcell + m.buffer.dequeue_fifo()),
    lambda m: set_mcell(m, m.mcell - m.buffer.dequeue_fifo()),
    lambda m: set_mcell(m, m.mcell * m.buffer.dequeue_fifo()),
    lambda m: set_mcell(m, m.mcell // m.buffer.dequeue_fifo()),
    lambda m: set_mcell(m, m.mcell & m.buffer.dequeue_fifo()),  # 20
    lambda m: set_mcell(m, m.mcell | m.buffer.dequeue_fifo()),
    lambda m: set_mcell(m, 1 if (m.mcell == 0) else 0),
    lambda m: set_mcell(m, m.mcell ^ m.buffer.dequeue_fifo()),
    lambda m: set_mcell(m, m.data_pointer),
    lambda m: set_mcell(m, m.ip + 1),  # 25
    lambda m: m.rel_jumpl(m.mcell),
    lambda m: m.rel_jumpr(m.mcell),
]
