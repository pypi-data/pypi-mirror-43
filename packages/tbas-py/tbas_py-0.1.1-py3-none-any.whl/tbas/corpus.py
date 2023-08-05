def load_string(in_str):
    program = '>'.join('+'*(ord(k)) for k in in_str)
    program += '<'*len(in_str)
    return program


def multiply_numbers(num1: int, num2: int, fudge: int = 0):
    program = '>' + '+'*max(num1, num2)
    program += '[<'
    program += '+'*min(num1, num2)
    program += '>-]'
    program += '<' + ('+'*fudge if (fudge > 0) else '-'*abs(fudge))
    return program
