
from solver import solve

from Encodings.Binomial_encoding import add_amo as binomial_amo
from Encodings.Commander_encoding import add_amo as commander_amo
from Encodings.Binary_encoding import add_amo as binary_amo
from Encodings.Product_encoding import add_amo as product_amo
from Encodings.Sequentialcounter import add_amo as sequential_amo

ENCODINGS = {
    "1": ("Binomial", binomial_amo),
    "2": ("Commander", commander_amo),
    "3": ("Binary", binary_amo),
    "4": ("Product", product_amo),
    "5": ("Sequential", sequential_amo),
}

def print_board(board):
    n = len(board)
    for row in board:
        print("|" + "".join(
            " Q |" if cell == 1 else " . |"
            for cell in row
        ))

def main():
    n = int(input("N = "))

    # Chọn Encoding:
    print("Encoding number:")
    for key, (name, _) in ENCODINGS.items():
        print(f"{key}. {name}")

    while True:
        choice = input("Encoding: ").strip()
        if choice in ENCODINGS:
            break

    encoding_name, add_amo = ENCODINGS[choice]
    result = solve(n, add_amo)

    print_board(result["solution"])
    print(f"SAT status: {result['satisfiable']}")
    print(f"Total time: {result['total_time']:.6f} seconds")

main()
