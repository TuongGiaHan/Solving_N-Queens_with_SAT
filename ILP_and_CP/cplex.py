
import sys
import time
from docplex.cp.model import CpoModel


def check(solution):
    if solution is None:
        return False

    n = len(solution)

    if sorted(solution) != list(range(n)):
        return False

    diag1 = [solution[i] - i for i in range(n)]
    diag2 = [solution[i] + i for i in range(n)]

    return len(set(diag1)) == n and len(set(diag2)) == n


def solve_cplex_cp(n, time_limit=None):
    model = CpoModel()

    q = [
        model.integer_var(min=0, max=n - 1, name=f"q_{i}")
        for i in range(n)
    ]

    model.add(model.all_diff(q))
    model.add(model.all_diff([q[i] + i for i in range(n)]))
    model.add(model.all_diff([q[i] - i for i in range(n)]))

    params = {}
    if time_limit is not None:
        params["TimeLimit"] = time_limit

    start = time.perf_counter()
    solution_result = model.solve(**params)
    elapsed = time.perf_counter() - start

    if solution_result is not None:
        solution = [
            solution_result.get_value(q[i])
            for i in range(n)
        ]
    else:
        solution = None

    return solution_result, elapsed, solution

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("ERROR")
        raise SystemExit(1)

    n = int(sys.argv[1])
    time_limit = float(sys.argv[2]) if len(sys.argv) == 3 else None

    if n < 4:
        raise ValueError("Pick N >= 4.")

    result, elapsed, solution = solve_cplex_cp(n, time_limit)
    valid = check(solution)

    print(f"Solver: CPLEX CP | N: {n} | Status: {result} | Time: {elapsed:.6f}s | Valid: {check(solution)}")