import math
from multiprocessing import Process, Pipe

class VectorMath:
    @staticmethod
    def dot_product(v1, v2):
        return sum(x * y for x, y in zip(v1, v2))

    @staticmethod
    def add(v1, v2):
        return [x + y for x, y in zip(v1, v2)]

    @staticmethod
    def sub(v1, v2):
        return [x - y for x, y in zip(v1, v2)]

    @staticmethod
    def scalar_mult(v, s):
        return [x * s for x in v]



class ConjugateGradientSolver:
    
    @staticmethod
    def _worker_process(conn):
        chunk = conn.recv()
        while True:
            p = conn.recv()
            if p is None:
                break
            res = [sum(x * y for x, y in zip(row, p)) for row in chunk]

            conn.send(res)

    def _partition_matrix(self, A, n, num_processes):
        chunk_size = math.ceil(n / num_processes)
        chunks = []
        for i in range(num_processes):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, n)
            if start < end:
                chunks.append(A[start:end])
        return chunks

    def _initialize_workers(self, chunks):
        pipes = []
        processes = []
        for chunk in chunks:
            parent_conn, child_conn = Pipe()
            pipes.append(parent_conn)
            
            p = Process(target=self._worker_process, args=(child_conn,))
            processes.append(p)
            p.start()
            
            parent_conn.send(chunk)
        return pipes, processes

    def _parallel_mat_vec_mult(self, pipes, p):
        for pipe in pipes:
            pipe.send(p)
            
        Ap = []
        for pipe in pipes:
            Ap.extend(pipe.recv())
        return Ap

    def _terminate_workers(self, pipes, processes):
        for pipe in pipes:
            pipe.send(None)
        for proc in processes:
            proc.join()

    def _cg_step(self, x, r, p, Ap, rs_old):
        alpha = rs_old / VectorMath.dot_product(p, Ap)
        x = VectorMath.add(x, VectorMath.scalar_mult(p, alpha))
        r = VectorMath.sub(r, VectorMath.scalar_mult(Ap, alpha))
        
        rs_new = VectorMath.dot_product(r, r)
        p = VectorMath.add(r, VectorMath.scalar_mult(p, rs_new / rs_old))
        
        return x, r, p, rs_new

    def solve_parallel(self, A, b, num_processes, tol=1e-10, max_iter=1000):
        n = len(b)
        chunks = self._partition_matrix(A, n, num_processes)
        pipes, processes = self._initialize_workers(chunks)

        x = [0.0] * n
        r = list(b)
        p = list(r)
        rs_old = VectorMath.dot_product(r, r)
        
        for k in range(max_iter):
            Ap = self._parallel_mat_vec_mult(pipes, p)
            x, r, p, rs_new = self._cg_step(x, r, p, Ap, rs_old)
            if math.sqrt(rs_new) < tol:
                break
            rs_old = rs_new
            
        self._terminate_workers(pipes, processes)
        return x
    
    def solve_serial(self, A, b, tol=1e-10, max_iter=1000):
        n = len(b)
        x = [0.0] * n
        r = list(b)
        p = list(r)
        rs_old = VectorMath.dot_product(r, r)
        
        for k in range(max_iter):
            Ap = [VectorMath.dot_product(row, p) for row in A]
            x, r, p, rs_new = self._cg_step(x, r, p, Ap, rs_old)
            if math.sqrt(rs_new) < tol:
                break
            rs_old = rs_new
            
        return x