import time
import os
from multiprocessing import cpu_count
from matrix_generator import MatrixManager
from matrix_solver import ConjugateGradientSolver

class App:
    def __init__(self):
        self.matrix_manager = MatrixManager(value_min=0, value_max=10, txt_max=50)
        self.solver = ConjugateGradientSolver()
        self.num_procs = cpu_count()
        self.results_dir = "results"
        os.makedirs(self.results_dir, exist_ok=True)

    def _save_solution(self, N, solution_vector, method_name, exec_time):
        n_folder = os.path.join(self.results_dir, str(N))
        os.makedirs(n_folder, exist_ok=True)
        
        filename = os.path.join(n_folder, f"{method_name}.txt")
        
        with open(filename, 'w') as f:
            f.write(f"N = {N}\n")
            f.write(f"{method_name}\n")
            f.write(f"Execution time {exec_time:.6f}\n")
            f.write("-" * 40 + "\n")
            for i, val in enumerate(solution_vector):
                f.write(f"x[{i}] = {val:.10f}\n")

    def _execute_tests(self, N):
        t0 = time.time()
        A, b = self.matrix_manager.get_or_create_matrix(N)
        print(f"\nДані завантажено за {time.time() - t0:.2f} сек.")
        
        print("\n--- Послідовне виконання ---")
        t0 = time.time()

        res_serial = self.solver.solve_serial(A, b)

        t_serial = time.time() - t0
        print(f"Час: {t_serial:.4f} сек.")
        
        print(f"\n--- Паралельне виконання ({self.num_procs} процесів) ---")
        t0 = time.time()

        res_parallel = self.solver.solve_parallel(A, b, self.num_procs)
        
        t_parallel = time.time() - t0
        print(f"Час: {t_parallel:.4f} сек.")

        self._save_solution(N, res_serial, "serial", t_serial)
        self._save_solution(N, res_parallel, "parallel", t_parallel)
        
        print("\n--- Порівняння швидкодії ---")
        if t_parallel > 0:
            speedup = t_serial / t_parallel
            print(f"Прискорення (Speedup): {speedup:.2f}x\n")
            print("=" * 50 + "\n")

    def run(self):
        print("Лабораторна робота №1. Варіант 16.")
        print("Введіть 0 щоб вийти.\n")
        
        while True:
            try:
                n_input = int(input("Введіть розмір матриці N: "))
            except ValueError:
                print("Введіть ціле число.")
                continue

            if n_input == 0:
                break
                
            self._execute_tests(n_input)

if __name__ == '__main__':
    app = App()
    app.run()