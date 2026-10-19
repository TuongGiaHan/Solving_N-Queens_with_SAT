
class CNFBuilder:
    def __init__(self, n: int):
        self.n = n
        self.clauses = []
        self.next_var = n * n + 1

    def add_clause(self, clause):
        self.clauses.append(list(clause))

    def new_var(self) -> int:
        variable = self.next_var
        self.next_var += 1
        return variable

    @property
    def num_vars(self) -> int:
        return self.next_var - 1


def get_board_groups(n: int):
    rows = [
        [(i * n + j + 1) for j in range(n)]
        for i in range(n)
    ]

    columns = [
        [(i * n + j + 1)for i in range(n)]
        for j in range(n)
    ]

    diagonal_diff = {}
    diagonal_sum = {}

    for i in range(n):
        for j in range(n):
            x = (i * n + j + 1)
            diagonal_diff.setdefault(i - j, []).append(x)
            diagonal_sum.setdefault(i + j, []).append(x)

    diagonals = [
        group
        for group in (
            list(diagonal_diff.values())
            + list(diagonal_sum.values())
        )
        if len(group) >= 2
    ]

    return rows, columns, diagonals