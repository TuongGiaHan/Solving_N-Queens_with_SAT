
def add_amo(builder, var):
    m = len(var)

    if m <= 1:
        return

    k = (m - 1).bit_length()
    bits = [builder.new_var() for _ in range(k)]

    for index, x in enumerate(var):
        for bit_index, bit_var in enumerate(bits):
            bit_is_one = (index >> bit_index) & 1

            if bit_is_one:
                builder.add_clause([-x, bit_var])
            else:
                builder.add_clause([-x, -bit_var])
