from constraints import CNFBuilder, get_board_groups


def build_nqueens_cnf(n, add_amo):
    if n < 1:
        raise ValueError("n must be at least 1")

    builder = CNFBuilder(n)
    rows, columns, diagonals = get_board_groups(n)

    # Exactly one queen in every row.
    for group in rows:
        add_amo(builder, group)    # AMO
        builder.add_clause(group)  # ALO

    # Exactly one queen in every column.
    for group in columns:
        add_amo(builder, group)    # AMO
        builder.add_clause(group)  # ALO

    # At most one queen on every diagonal.
    for group in diagonals:
        add_amo(builder, group)

    return builder