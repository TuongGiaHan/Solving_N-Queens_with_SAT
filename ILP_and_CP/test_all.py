import csv
import time
from pathlib import Path

from ILP_and_CP.ilp_nq import solve_gurobi, solve_cplex, check as check_ilp
from ILP_and_CP.cp_sat import solve_cp_sat, check as check_cp_sat
from ILP_and_CP.cplex import solve_cplex_cp, check as check_cplex


SOLVERS = ["Gurobi MIP", "CPLEX MIP", "CPLEX CP", "CP-SAT"]
N_VALUES = [4, 8, 12, 16, 25, 27, 36, 64, 81, 100, 135, 216, 343, 512, 729, 1000, 1024, 1331]
TIME_LIMIT = 60.0
OUTPUT_FILE = "exact_solver.csv"


def run_solver(solver_name, n, time_limit):
    start = time.perf_counter()
    try:
        if solver_name == "Gurobi MIP":
            status, _, solution = solve_gurobi(n, time_limit)
            valid = check_ilp(solution)
        elif solver_name == "CPLEX MIP":
            status, _, solution = solve_cplex(n, time_limit)
            valid = check_ilp(solution)
        elif solver_name == "CPLEX CP":
            status, _, solution = solve_cplex_cp(n, time_limit)
            valid = check_cplex(solution)
        elif solver_name == "CP-SAT":
            status, _, solution = solve_cp_sat(n, time_limit)
            valid = check_cp_sat(solution)
    except Exception as exc:
        status, solution, valid = f"ERROR_{type(exc).__name__}", None, False

    elapsed = time.perf_counter() - start

    if "LICENSE" in str(status).upper() or "LIMIT" in str(status).upper():
        classification = "LICENSE_LIMIT"
    elif "TIME" in str(status).upper() or elapsed >= time_limit * 0.98:
        classification = "TIMEOUT"
    elif solution is not None and valid:
        classification = "VALID_SOLUTION"
    else:
        classification = status

    return classification, round(elapsed, 6)


def main():
    stopped = {}  
    results = []

    fields = ["N", "Solver", "Classification", "Runtime_s"]

    for n in N_VALUES:
        for solver in SOLVERS:
            if solver in stopped:
                results.append({
                    "N": n,
                    "Solver": solver,
                    "Classification": f"SKIPPED_{stopped[solver]}",
                    "Runtime_s": ""
                })
                continue

            print(f"Testing N={n:4d} | Solver={solver:10s} ... ", end="", flush=True)
            classification, elapsed = run_solver(solver, n, TIME_LIMIT)
            print(f"Status={classification}, Time={elapsed}s")

            results.append({
                "N": n,
                "Solver": solver,
                "Classification": classification,
                "Runtime_s": elapsed if classification == "VALID_SOLUTION" else ""
            })

            if classification in ("LICENSE_LIMIT", "TIMEOUT"):
                stopped[solver] = classification

    with Path(OUTPUT_FILE).open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nHoàn tất")


if __name__ == "__main__":
    main()