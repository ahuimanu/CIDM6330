"""Kata6: multiprocessing data processing example

Implements:
- data generation and chunking
- per-chunk CPU-bound processing
- progress reporting
- worker failure handling with a single retry

Run via the runner `run_kata6.py`.
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Dict
import argparse
import math


def generate_data(n: int) -> List[int]:
    return list(range(1, n + 1))


def chunked(data: List[int], chunk_size: int):
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def process_chunk(chunk: List[int]) -> Dict[str, int]:
    # CPU-bound simulated work
    heavy = 0
    for x in chunk:
        # some intentionally expensive operations that are deterministic
        for i in range(1, 200):
            heavy += (x * i) % (i + 1)
        # a math op to keep CPU busy
        _ = math.sqrt(x + 0.0001)
    return {"count": len(chunk), "sum": sum(chunk), "heavy": heavy}


def run(total_items: int = 5000, chunk_size: int = 500, workers: int | None = None):
    data = generate_data(total_items)
    chunks = list(chunked(data, chunk_size))
    total_chunks = len(chunks)

    aggregated = {"count": 0, "sum": 0, "heavy": 0}
    completed = 0

    # map chunk id -> retries
    retries = {i: 0 for i in range(total_chunks)}
    max_retries = 1

    with ProcessPoolExecutor(max_workers=workers) as ex:
        futures = {}
        for idx, chunk in enumerate(chunks):
            futures[ex.submit(process_chunk, chunk)] = (idx, chunk)

        while futures:
            for fut in list(as_completed(futures, timeout=0.1)):
                idx, chunk = futures.pop(fut)
                try:
                    res = fut.result()
                except Exception as e:
                    print(f"Chunk {idx} failed: {e}")
                    if retries[idx] < max_retries:
                        retries[idx] += 1
                        print(f"Retrying chunk {idx} (attempt {retries[idx]})")
                        futures[ex.submit(process_chunk, chunk)] = (idx, chunk)
                    else:
                        print(f"Skipping chunk {idx} after {max_retries} retries")
                    continue

                aggregated["count"] += res["count"]
                aggregated["sum"] += res["sum"]
                aggregated["heavy"] += res["heavy"]
                completed += 1
                print(f"Progress: {completed}/{total_chunks} chunks completed")

    print("--- Final aggregation ---")
    print(f"Total items processed: {aggregated['count']}")
    print(f"Sum of items: {aggregated['sum']}")
    print(f"Heavy aggregate value: {aggregated['heavy']}")
    return aggregated


def cli():
    p = argparse.ArgumentParser(description="Kata6 multiprocessing example")
    p.add_argument("--items", type=int, default=5000)
    p.add_argument("--chunk", type=int, default=500)
    p.add_argument("--workers", type=int, default=None)
    args = p.parse_args()
    run(total_items=args.items, chunk_size=args.chunk, workers=args.workers)


if __name__ == "__main__":
    cli()
