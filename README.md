# Bai_Tap_Lon_1_N-Queens_Problems

## Introduction
Đây là source code cho Bài tập lớp 1 của lớp 2627I_INT3011E_4: Các vấn đề hiện đại trong KHMT. 
Chủ đề: SAT Encoding for Logic puzzles, N-Queens. Đề tài được chọn là N-Queens solver, với Yêu cầu cài đặt solver giải bài toán N-Queens, dùng các SAT solver tại thư viện PySAT để giải. 

Các triển khai trong bài báo cáo bao gồm:

- Xây dựng và cài đặt triển khai các phương pháp cài đặt SAT Encoding cho AMO và ALO, bao gồm: Binomial, Binary, Commander, Product, Sequential Counter, sử dụng thư viện PySAT để hỗ trợ.

- Kiểm thử ma trận lớn

- Bài báo cáo BTL:

- So sánh phương pháp giải SAT Encoding với phương pháp giải chính xác khác như ILP, CP, so sánh với Cpelx CP, Cplex MIP, Gurobi và CP-SAT.

## Cấu trúc dự án:

```
nQueens-SAT/
├── Encodings/
│   ├── Binomial_encoding.py #AMO của Binomial
│   ├── Binary_encoding.py #AMO của Binary
│   ├── Commander_encoding.py #AMO của Commander
│   ├── Sequential_counter.py #AMO của Sequential Counter
│   └── Product_encoding.py #AMO của Product
├── ILP_and_CP/
│   ├── cp_sat.py # CP và bộ giải CP-SAT
│   ├── cplex.py # CP và bộ giải Cplex CP
│   ├── ilp_nq.py # ILP và bộ giải Gurobi + Cplex MIP
│   ├── test_all.py #test 3 file trên 
├── constraints.py #định nghĩa ràng buộc
├── nqueens.py  #quy trình giải bài toán (AMO/ALO hàng, cột, đường chéo)
├── solver.py #Kết hợp ràng buộc và phương thức, gọi bộ giải SAT
├── main.py  #chương trình chính 
├── test.py  #sử dụng để test nhiều Encoding
└── README.md
```

## Các công cụ sử dụng:
Bài chạy trên VS Code có:

1, Python enviroment

2, Thư viện PySAT - cho SAT Solving, tích hợp Glucose3

3, Các thư viện Cpelx CP, Cplex MIP, Gurobi và CP-SAT (bản miễn phí cài đặt)

## Cài đặt môi trường:
+) PySAT

Chạy trong Terminal VS Code:

python -m pip install python-sat

hoặc

python -m pip install --upgrade pip

python -m pip install python-sat

+) OR-Tools CP-SAT:

Chạy trong Terminal VS Code:

python -m pip install ortools

+) Gurobi:

Chạy trong Terminal VS Code:

python -m pip install gurobipy

+) Cplex MIP và DOcplex (Cplex CP):

Chạy trong Terminal VS Code:

python -m pip install cplex docplex



Thông thường khi cài đặt sẽ có thông báo liên quan đến bản quyển (cho phép chạy bài toán nhỏ cho bản quyền free)



## Chạy bài toán:

1, Sử dụng file main.py, chạy file hoặc nhận vào terminal python main.py.

Main sẽ hỏi kích thước N và Encoding muốn sử dụng. Ta có thể chọn Encoding nhờ việc các Encoding dùng chung các ALO và format, ta chỉ cần viết AMO. Do đó, file nqueens.py được gọi chính là cấu trúc triển khai bài toán SAT

2, Khi muốn thử nghiệm số lớn, ta có 2 file test.py và test_all.py. Test.py có mảng N = {4, 8, 12, 16, 25, 27, 36, 64, 81, 100, 135, 216, 343, 512, 729, 1000, 1024, 1331 } có sẵn để test với 5 Encoding, còn test_all.py có mảng N = {4, 8, 12, 16, 25, 27, 36, 64, 81, 100, 135, 216, 343, 512 }, ít hơn do ta sẽ không chạy kích thước quá lớn khi tất cả đều fail ở kích thước trung bình.

Chạy file hoặc nhập vào terminal python test.py / python test_all.py

Hai file sau khi chạy sẽ lưu vào benchmark_results.csv và benchmark_ilp_cp.csv


## 
