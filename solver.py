
from time import perf_counter

from pysat.solvers import Glucose3
from nqueens import build_nqueens_cnf


def solve(n, add_amo):
    total_start = perf_counter()

    encoding_start = perf_counter()
    builder = build_nqueens_cnf(n, add_amo)
    encoding_time = perf_counter() - encoding_start

    setup_start = perf_counter()
    with Glucose3(bootstrap_with=builder.clauses) as solver:
        solver_setup_time = perf_counter() - setup_start

        solve_start = perf_counter()
        satisfiable = solver.solve()
        solving_time = perf_counter() - solve_start

        model = solver.get_model() if satisfiable else None

    board = None

    if model is not None:
        true_variables = {
            literal for literal in model if literal > 0
        }

        board = [
            [
                int((i * n + j + 1) in true_variables)
                for j in range(n)
            ]
            for i in range(n)
        ]

    total_time = perf_counter() - total_start

    return {
        "solution": board,
        "satisfiable": satisfiable,
        "num_vars": builder.num_vars,
        "num_clauses": len(builder.clauses),
        "encoding_time": encoding_time,
        "solver_setup_time": solver_setup_time,
        "solving_time": solving_time,
        "time": solver_setup_time + solving_time,
        "total_time": total_time,
    }
