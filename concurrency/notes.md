
n.bit_length()

with ProcessPoolExecutor() as pool:
    partial = list(pool.map(ClassName.fn_name, zipped_args))

def chunk(self, data: List[float]) -> List[List[float]]:
    n = len(data)
    workers = min(self.max_workers, n)
    chunk_sz = n // workers
    rem = n % workers
    cs = [i * chunk_sz + min(i, rem) for i in range(workers+1)]
    return [data[cs[i]: cs[i+1]] for i in range(workers)]

