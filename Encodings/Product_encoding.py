from math import ceil, sqrt

def add_amo(builder, var):
    global cur_var
    m = len(var)
    p = ceil(sqrt(m));
    q = (m + p - 1) // p

    row_vars = [builder.new_var() for _ in range(p)]
    col_vars = [builder.new_var() for _ in range(q)]

    for index, x in enumerate(var):
        row, col = index // q, index % q;

        builder.add_clause([-x, row_vars[row]])
        builder.add_clause([-x, col_vars[col]])

    n = len(row_vars)
    for i in range(n):
        for j in range(i+1,n):
            x = row_vars[i]
            y = row_vars[j]
            builder.add_clause([-x, -y])

    n = len(col_vars)
    for i in range(n):
        for j in range(i+1,n):
            x = col_vars[i]
            y = col_vars[j]
            builder.add_clause([-x, -y])

