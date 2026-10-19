import sys
import time
from ortools.sat.python import cp_model


def check(solution):
    if not solution:
        return False
    n = len(solution)
    return (
        len(set(solution)) == n
        and len({solution[i] - i for i in range(n)}) == n
        and len({solution[i] + i for i in range(n)}) == n
    )


def solve_cp_sat(n, time_limit=None):
    model = cp_model.CpModel()
    q = [model.new_int_var(0, n - 1, f"q_{i}") for i in range(n)]

    model.add_all_different(q)
    model.add_all_different([q[i] + i for i in range(n)])
    model.add_all_different([q[i] - i for i in range(n)])

    solver = cp_model.CpSolver()
    if time_limit is not None:
        solver.parameters.max_time_in_seconds = time_limit

    start = time.perf_counter()
    status = solver.solve(model)
    elapsed = time.perf_counter() - start

    status_name = solver.status_name(status)
    solution = [solver.value(q[i]) for i in range(n)] if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None

    return status_name, elapsed, solution


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR")
        sys.exit(1)

    n = int(sys.argv[1])
    time_limit = float(sys.argv[2]) if len(sys.argv) >= 3 else None

    status, elapsed, solution = solve_cp_sat(n, time_limit)
    print(f"Solver: CP-SAT | N: {n} | Status: {status} | Time: {elapsed:.6f}s | Valid: {check(solution)}")