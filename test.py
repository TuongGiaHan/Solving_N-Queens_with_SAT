
import csv
import multiprocessing as mp
import time

from solver import solve

from Encodings.Binomial_encoding import add_amo as binomial
from Encodings.Binary_encoding import add_amo as binary
from Encodings.Commander_encoding import add_amo as commander
from Encodings.Product_encoding import add_amo as product
from Encodings.Sequentialcounter import add_amo as sequential_counter


ENCODINGS = {
    "Binomial": binomial,
    "Binary": binary,
    "Commander": commander,
    "Sequential Counter": sequential_counter,
    "Product": product
}

N_VALUES = [
    4, 8, 12, 16, 25, 27, 36,
    64, 81, 100, 135, 216, 343, 
    512, 729, 1000, 1024, 1331
]
TIMEOUT_SECONDS = 120
OUTPUT_FILE = "benchmark_results.csv"

def run_one(n, encoding_name, result_queue):
    try:
        add_amo = ENCODINGS[encoding_name]
        result = solve(n, add_amo)

        result_queue.put({
            "status": "SAT" if result["satisfiable"] else "UNSAT",
            "variables": result["num_vars"],
            "clauses": result["num_clauses"],
            "encoding_time": result["encoding_time"],
            "setup_time": result["solver_setup_time"],
            "solving_time": result["solving_time"],
            "total_time": result["total_time"],
        })

    except Exception as exc:
        result_queue.put({
            "status": "ERROR",
            "error": repr(exc),
        })


def run(n, encoding_name, timeout_seconds):
    result_queue = mp.Queue()
    process = mp.Process(
        target=run_one,
        args=(n, encoding_name, result_queue),
    )

    start = time.perf_counter()
    process.start()
    process.join(timeout_seconds)
    elapsed = time.perf_counter() - start

    if process.is_alive():
        process.terminate()
        process.join()
        result = {
            "status": "TIMEOUT",
            "elapsed": elapsed,
            "variables": "",
            "clauses": "",
            "encoding_time": "",
            "setup_time": "",
            "solving_time": "",
        }
    else :
        try:
            result = result_queue.get(timeout=2)
        except Exception:
            result = {
                "status": "ERROR",
                "error": f"Worker exited with code {process.exitcode}",
            }

        result["elapsed"] = elapsed
        
    result_queue.close()
    return result


def main():
    fields = [
        "N",
        "Encoding",
        "Status",
        "Variables",
        "Clauses",
        "Encoding_Time_s",
        "Solver_Setup_Time_s",
        "Solving_Time_s",
        "Elapsed_Time_s",
        "Error",
    ]

    with open(
        OUTPUT_FILE, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for encoding_name in ENCODINGS:
            print(f"\n===== {encoding_name} =====")

            for n in N_VALUES:
                print(
                    f"Testing N={n}, encoding={encoding_name}...",
                    flush=True,
                )

                result = run(
                    n, encoding_name, TIMEOUT_SECONDS
                )

                row = {
                    "N": n,
                    "Encoding": encoding_name,
                    "Status": result["status"],
                    "Variables": result.get("variables", ""),
                    "Clauses": result.get("clauses", ""),
                    "Encoding_Time_s": result.get("encoding_time", ""),
                    "Solver_Setup_Time_s": result.get("setup_time", ""),
                    "Solving_Time_s": result.get("solving_time", ""),
                    "Elapsed_Time_s": round(result["elapsed"], 6),
                    "Error": result.get("error", ""),
                }

                writer.writerow(row)
                file.flush()

                print(
                    f"  Status={result['status']}, "
                    f"elapsed={result['elapsed']:.2f}s",
                    flush=True,
                )

                if (result["status"] == "TIMEOUT" and encoding_name != "Product") or  (result["status"] == "ERROR" and encoding_name != "Product"):
                    print(f"==> {encoding_name} bị TIMEOUT ở N={n}")
                    break

    print(f"\nResults saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    mp.freeze_support()
    main()
