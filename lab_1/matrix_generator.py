import random
import os
import pickle

class MatrixManager:
    def __init__(self, folder_name="matrices", value_min=0, value_max=100, txt_max=50):
        self.folder_name = folder_name
        self.value_min = value_min
        self.value_max = value_max
        self.txt_max = txt_max
        
        self.pkl_folder = os.path.join(self.folder_name, "pkl")
        self.txt_folder = os.path.join(self.folder_name, "txt")
        
        os.makedirs(self.folder_name, exist_ok=True)
        os.makedirs(self.pkl_folder, exist_ok=True)
        os.makedirs(self.txt_folder, exist_ok=True)

    def _generate_spd_matrix(self, n):
        sym_matrix = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i, n):
                val = random.randint(self.value_min, self.value_max)
                sym_matrix[i][j] = val
                sym_matrix[j][i] = val 
                
        for i in range(n):
            sym_matrix[i][i] += n * self.value_max
            
        b = [random.randint(self.value_min, self.value_max) for _ in range(n)]
        
        return sym_matrix, b

    def _get_matrix(self, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data['A'], data['b']

    def _create_matrix(self, n, pkl_filename):
        print(f"Генерація нової матриці {n}x{n}")
        A, b = self._generate_spd_matrix(n)
        
        with open(pkl_filename, 'wb') as f:
            pickle.dump({'A': A, 'b': b}, f)
            
        if n <= self.txt_max:
            txt_filename = os.path.join(self.txt_folder, f"matrix_{n}.txt")
            
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(f"matrix A ({n}x{n}):\n")
                for row in A:
                    f.write(" ".join(f"{val:6}" for val in row) + "\n")
                
                f.write("\nVector b:\n")
                f.write(" ".join(f"{val:6}" for val in b) + "\n")
        
        return A, b

    def get_or_create_matrix(self, n):
        pkl_filename = os.path.join(self.pkl_folder, f"matrix_{n}.pkl")
        
        if os.path.exists(pkl_filename):
            return self._get_matrix(pkl_filename)
        else:
            return self._create_matrix(n, pkl_filename)