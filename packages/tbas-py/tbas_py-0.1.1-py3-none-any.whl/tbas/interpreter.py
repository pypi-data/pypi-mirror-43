from tbas.machine import Machine


def interpret_program(program_string: str, machine: Machine = None, t=65536):
    if machine is None:
        machine = Machine()
    timeout = t
    machine.load_program(program_string)

    should_continue = True

    while should_continue and timeout > 0:
        try:
            should_continue = machine.step_once()
        except Exception as e:
            machine.debug_printout()
            raise e
        timeout -= 1
    print()
    if timeout == 0:
        machine.debug_printout()
        assert False, "Program used too many cycles"

def main():
    ins = input("> ")
    if ins == 'exit':
      exit()
    interpret_program(ins)


if __name__ == '__main__':
    main()
