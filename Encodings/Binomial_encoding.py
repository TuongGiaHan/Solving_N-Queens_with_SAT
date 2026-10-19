
def add_amo(builder, var):
    m = len(var)

    for i in range(m):
        for j in range(i + 1, m):
            builder.add_clause([
                -var[i],
                -var[j]
            ])
