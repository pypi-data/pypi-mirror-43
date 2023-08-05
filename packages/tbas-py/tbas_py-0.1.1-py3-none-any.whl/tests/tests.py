import unittest
from tbas.machine import Machine


class TestLanguage(unittest.TestCase):

    def test_mptr_inc_dec(self):
        m = Machine(program='+++>+++>+++>++++')
        m.run()
        self.assertEqual(3, m.mem_at(0))
        self.assertEqual(3, m.mem_at(1))
        self.assertEqual(3, m.mem_at(2))
        self.assertEqual(4, m.mcell)
        m.reset_program()
        m.load_program('>>>-<--<---<----')
        m.run()
        self.assertEqual(0, m.mcell)
        self.assertEqual(0, m.mem_at(1))
        self.assertEqual(1, m.mem_at(2))
        self.assertEqual(3, m.mem_at(3))

    def test_loop(self):
        m = Machine(program='+++++')
        self.assertEqual(5, m.run())
        self.assertEqual(5, m.mem_at(0))
        m.reset_program()
        m.load_program('[-]')
        self.assertEqual(11, m.run())
        self.assertEqual(0, m.mcell)

    def test_nested_loop(self):
        m = Machine(program='+++++[>+++[>+<-]<-]')
        m.run()
        self.assertEqual(15, m.mem_at(2))


class TestBuffer(unittest.TestCase):

    def test_buffer_program(self):
        m = Machine()
        program_string = '++++++=?'
        m.load_program(program_string)
        m.run()
        self.assertEqual(program_string, str(m.buffer))

    def test_buffer_filo(self):
        m = Machine(program='+'*8 + '=?-?-?-?-?-?-?-?' + '+'*8 + '=>?>?>?>?>?>?>?>?')
        m.run()
        self.assertEqual(9, m.mem_at(0))
        for i in range(1, 9):
            self.assertEqual(i, m.mem_at(i))

    def test_buffer_fifo(self):
        m = Machine(program='+'*8 + '=?-?-?-?-?-?-?-?' + '+'*9 + '=->?>?>?>?>?>?>?>?')
        m.run()
        for i in range(9, 0, -1):
            self.assertEqual(i, m.mem_at(9 - i))

    def test_quine(self):
        m = Machine(program='++++++=?+=>?')
        m.run()
        m = Machine(program='++++++=?++++=>++>+[?<=>?<<=>>]<<----=?+=>>>?')
        m.run()
        self.assertTrue(True)


class TestConversions(unittest.TestCase):

    def test_ascii_lowercase(self):
        m = Machine()
        from string import ascii_lowercase
        program = '+'*12 + '=' + '-'*12 + '>'.join('+'*i for i in range(len(ascii_lowercase)))
        program += '<'*(program.count('>'))
        program += '>'.join('?' for _ in range(len(ascii_lowercase)))
        m.load_program(program)
        m.run()
        for index, val in enumerate(ascii_lowercase):
            self.assertEqual(ord(val), m.mem_at(index))

    def test_ascii_uppercase(self):
        m = Machine()
        from string import ascii_uppercase
        program = '+'*13 + '=' + '-'*13 + '>'.join('+'*i for i in range(len(ascii_uppercase)))
        program += '<'*(program.count('>'))
        program += '>'.join('?' for _ in range(len(ascii_uppercase)))
        m.load_program(program)
        m.run()
        for index, val in enumerate(ascii_uppercase):
            self.assertEqual(ord(val), m.mem_at(index))

    def test_digits(self):
        m = Machine()
        from string import digits
        program = '+'*14 + '=' + '-'*14 + '>'.join('+'*i for i in range(len(digits)))
        program += '<'*(program.count('>'))
        program += '>'.join('?' for _ in range(len(digits)))
        m.load_program(program)
        m.run()
        for index, val in enumerate(digits):
            self.assertEqual(ord(val), m.mem_at(index))

    def test_tbas(self):
        m = Machine()
        from tbas.badge_io import tbas_chars
        program = '+'*15 + '=' + '-'*15 + '>'.join('+'*i for i in range(len(tbas_chars)))
        program += '<'*(program.count('>'))
        program += '>'.join('?' for _ in range(len(tbas_chars)))
        m.load_program(program)
        m.run()
        for index, val in enumerate(tbas_chars):
            self.assertEqual(ord(val), m.mem_at(index))


class TestALU(unittest.TestCase):

    def test_add(self):
        m = Machine(program='++++++++=?++++++++=?')
        m.run()
        self.assertEqual(16+8, m.mcell)

    def test_sub(self):
        m = Machine(program='++++++++=?+++++++++=?')
        m.run()
        self.assertEqual(17-8, m.mcell)

    def test_mul(self):
        m = Machine(program='++++++++=?++++++++++=?')
        m.run()
        self.assertEqual(18*8, m.mcell)

    def test_div(self):
        m = Machine(program='++++++++=?+++++++++++=+++++?')
        m.run()
        self.assertEqual(24//8, m.mcell)

    def test_and(self):
        m = Machine(program='++++++++=?++++++++++++=?')
        m.run()
        self.assertEqual(20 & 8, m.mcell)

    def test_or(self):
        m = Machine(program='++++++++=?+++++++++++++=?')
        m.run()
        self.assertEqual(21 | 8, m.mcell)

    def test_not(self):
        m = Machine(program='++++++++=?++++++++++++++=?')
        m.run()
        self.assertEqual(0, m.mcell)

    def test_xor(self):
        m = Machine(program='++++++++=?+++++++++++++++=?')
        m.run()
        self.assertEqual(23 ^ 8, m.mcell)


class TestMeta(unittest.TestCase):

    def test_mptr(self):
        m = Machine(program='+'*24 + '=>>>?')
        m.run()
        self.assertEqual(m.data_pointer, m.mcell)

    def test_eptr(self):
        m = Machine(program='+'*25 + '=>>>?')
        m.run()
        self.assertEqual(m.ip, m.mcell)

    def test_reljump_left(self):
        m = Machine(program='>+<' + '+'*26 + '=' + '-'*26 + '+'*10 + '>[-<?]<')
        m.run()
        self.assertEqual(15, m.mcell)
        # TODO: Figure out if this should be 15 or 16. The emulator increments the
        # instruction pointer after a jump. I'm not sure if TBAS does this on hardware.

    def test_reljump_right(self):
        m = Machine(program='+'*27 + '=' + '-'*20 + '?' + '+'*10)
        m.run()
        self.assertEqual(10, m.mcell)


class TestInterpreter(unittest.TestCase):

    def test_exceptions(self):
        from tbas.interpreter import interpret_program
        with self.assertRaises(AssertionError):
            interpret_program('Q')

        with self.assertRaises(AssertionError):
            interpret_program('+++++', t=4)

    def test_user_input(self):
        import sys, io
        from tbas import interpreter
        stdin = sys.stdin
        sys.stdin = io.StringIO("3\n")
        interpreter.interpret_program('+=?>=<?')
        sys.stdin = io.StringIO("c\n")
        interpreter.interpret_program('+++=?>++=<?')
        sys.stdin = stdin


class TestCorpus(unittest.TestCase):

    def test_string_loading(self):
        from tbas.corpus import load_string

        target_str = "Spammish Repetition"
        m = Machine(program=load_string(target_str))
        m.run()
        self.assertEqual(target_str, str(m))

    def test_multiply(self):
        from tbas.corpus import multiply_numbers

        m = Machine(program=multiply_numbers(3, 5))
        m.run()
        self.assertEqual(15, m.mcell)

        m.clean_init()
        m.load_program(multiply_numbers(5, 8, 2))
        m.run()
        self.assertEqual(42, m.mcell)

        m.clean_init()
        m.load_program(multiply_numbers(10, 7, -1))
        m.run()
        self.assertEqual(69, m.mcell)  # nice


def main():
    unittest.main()


if __name__ == '__main__':
    main()
