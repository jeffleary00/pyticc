
def byte_bit_value(byte, schema):
    """
    Extract bit(s) value from a byte.

    BYTE INDEX =  | 0 | 1 | 2 | 3 || 4 | 5 | 6 | 7 |
                 msb                              lsb
                 128                               1

    args:
        - byte value(int)
        - data schema(list): [index, bits]
          - data's starting bit index.
          - number of bits.

    returns:
        int
    """

    index, bits = schema

    if index < 0 or index > 7:
        raise ValueError("Schema index must be 0 thru 7")
    if bits < 1 or bits > 8:
        raise ValueError("Schema bits must be 1 thru 8")
    if len( list(bin(byte)[2:]) ) > 8:
        raise ValueError("Number too big. Not a byte value.")

    if index == 0 and bits == 8:
        # nothing to do
        return byte

    shift = 8 - (index + bits)
    mask = 0xFF >> (shift + index)
    return byte >> shift & mask


def bit_into_byte(byte, schema, value):
    """
    Update bits in a byte to get new value.

    args:
        - initial byte we are working with.
        - data schema(list): [index, bits]
          - data's starting bit index.
          - number of bits.
        - new value for target.
    returns:
        new byte value (int)
    """

    if type(value) is str:
        # user passed in string with bits, like "1011"?
        value = int(value, 2)

    index, bits = schema

    if index < 0 or index > 7:
        raise ValueError("Schema index must be 0 thru 7")
    if bits < 1 or bits > 8:
        raise ValueError("Schema bits must be 1 thru 8")
    if len(list(bin(byte)[2:])) > 8 or len(list(bin(value)[2:])) > 8:
        raise ValueError("Number too big. Not a byte value.")

    orig_bits = list(bin(byte)[2:].zfill(8))
    value_bits = list(bin(value)[2:].zfill(bits))

    for i in range(0, bits):
        orig_bits[index + i] = value_bits[i]

    return int("".join(orig_bits), 2)
