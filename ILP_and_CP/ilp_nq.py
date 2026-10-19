import sys
import time


def check(solution):
    if not solution:
        return False
    n = len(solution)
    return (
        len(set(solution)) == n
        and len({solution[i] - i for i in range(n)}) == n
        and len({solution[i] + i for i in range(n)}) == n
    )


def solve_gurobi(n, time_limit=None):
    import gurobipy as gp
    from gurobipy import GRB

    try:
        model = gp.Model("NQueens_MIP")
        model.Params.OutputFlag = 0
        if time_limit is not None:
            model.Params.TimeLimit = float(time_limit)

        x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

        for i in range(n):
            model.addConstr(gp.quicksum(x[i, j] for j in range(n)) == 1)
            model.addConstr(gp.quicksum(x[j, i] for j in range(n)) == 1)

        for d in range(-(n - 1), n):
            model.addConstr(gp.quicksum(x[i, j] for i in range(n) for j in range(n) if i - j == d) <= 1)
        for s in range(2 * n - 1):
            model.addConstr(gp.quicksum(x[i, j] for i in range(n) for j in range(n) if i + j == s) <= 1)

        model.setObjective(0, GRB.MINIMIZE)

        start = time.perf_counter()
        model.optimize()
        elapsed = time.perf_counter() - start

        if model.SolCount > 0:
            solution = [next(j for j in range(n) if x[i, j].X > 0.5) for i in range(n)]
            status = "OPTIMAL" if model.Status == GRB.OPTIMAL else "FEASIBLE"
            return status, elapsed, solution

        status = "TIME_LIMIT" if model.Status == GRB.TIME_LIMIT else f"STATUS_{model.Status}"
        return status, elapsed, None

    except Exception as exc:
        err_msg = str(exc).upper()
        if "LICENSE" in err_msg or "LIMIT" in err_msg or "RESTRICTED" in err_msg:
            return "LICENSE_LIMIT", 0.0, None
        return f"ERROR_{type(exc).__name__}", 0.0, None


def solve_cplex(n, time_limit=None):
    from docplex.mp.model import Model

    try:
        model = Model(name="NQueens_MIP")
        model.context.solver.log_output = False
        if time_limit is not None:
            model.set_time_limit(float(time_limit))

        x = {(i, j): model.binary_var(name=f"x_{i}_{j}") for i in range(n) for j in range(n)}

        for i in range(n):
            model.add_constraint(model.sum(x[i, j] for j in range(n)) == 1)
            model.add_constraint(model.sum(x[j, i] for j in range(n)) == 1)

        for d in range(-(n - 1), n):
            model.add_constraint(model.sum(x[i, j] for i in range(n) for j in range(n) if i - j == d) <= 1)
        for s in range(2 * n - 1):
            model.add_constraint(model.sum(x[i, j] for i in range(n) for j in range(n) if i + j == s) <= 1)

        model.minimize(0)

        start = time.perf_counter()
        sol = model.solve()
        elapsed = time.perf_counter() - start

        if sol is not None:
            solution = [next(j for j in range(n) if sol.get_value(x[i, j]) > 0.5) for i in range(n)]
            status = "OPTIMAL"
            return status, elapsed, solution

        details = str(getattr(model.solve_details, 'status', '')).upper()
        status = "TIME_LIMIT" if "TIME" in details or "LIMIT" in details else "NO_SOLUTION"
        return status, elapsed, None

    except Exception as exc:
        err_msg = str(exc).upper()
        if "LICENSE" in err_msg or "LIMIT" in err_msg or "PROMOTIONAL" in err_msg or "MANY ELEMENTS" in err_msg:
            return "LICENSE_LIMIT", 0.0, None
        return f"ERROR_{type(exc).__name__}", 0.0, None


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERROR")
        sys.exit(1)

    backend = sys.argv[1].lower()
    n = int(sys.argv[2])
    time_limit = float(sys.argv[3]) if len(sys.argv) >= 4 else None

    if backend == "gurobi":
        status, elapsed, solution = solve_gurobi(n, time_limit)
    elif backend == "cplex":
        status, elapsed, solution = solve_cplex(n, time_limit)
    else:
        raise ValueError("Backend must be 'gurobi' or 'cplex'")

    print(f"Solver: {backend.upper()} MIP | N: {n} | Status: {status} | Time: {elapsed:.6f}s | Valid: {check(solution)}")