
def add_amo(builder, var):
    m = len(var)

    if m <= 1:
        return

    s = [builder.new_var() for _ in range(m - 1)]
    builder.add_clause([-var[0], s[0]])

    for i in range(1, m - 1):
        x = var[i]

        builder.add_clause([-x, s[i]])
        builder.add_clause([-s[i - 1], s[i]])
        builder.add_clause([-x, -s[i - 1]])

    builder.add_clause([-var[-1], -s[-1]])
