from tbas.datatypes import Memory


def debug_buffer(buffer: Memory, indent: int = 0, delimiter: str='  '):
    indices = " "*indent + "IDX: "
    integers = " "*indent + "INT: "
    chars = " "*indent + "CHR: "
    indices += delimiter.join(("{:>3d}".format(i) if (i % 5 == 0) else '   ') for i in range(len(buffer)))
    integers += delimiter.join("{:>3d}".format(k) for k in buffer)
    chars += delimiter.join("{:>3s}".format(chr(k) if k > 31 else '_') for k in buffer)
    print(indices)
    print(integers)
    print(chars)
