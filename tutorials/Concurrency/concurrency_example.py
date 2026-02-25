"""
Concurrency Fundamentals Example

This module demonstrates Python's concurrency options:
1. Threading - for I/O-bound tasks
2. Multiprocessing - for CPU-bound tasks  
3. concurrent.futures - high-level interface
4. asyncio - cooperative multitasking

Run with: python example.py
"""

import threading
import multiprocessing
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from queue import Queue
from typing import Callable


# =============================================================================
# DOMAIN MODEL
# =============================================================================


@dataclass
class Airport:
    stationid: str
    name: str
    city: str
    state: str


@dataclass
class WeatherReport:
    stationid: str
    temperature: float
    conditions: str


# Sample data
AIRPORTS = [
    Airport("KAMA", "Rick Husband Amarillo International", "Amarillo", "TX"),
    Airport("KLBB", "Lubbock Preston Smith International", "Lubbock", "TX"),
    Airport("KMAF", "Midland International Air and Space Port", "Midland", "TX"),
    Airport("KDFW", "Dallas/Fort Worth International", "Dallas", "TX"),
    Airport("KHOU", "William P. Hobby Airport", "Houston", "TX"),
    Airport("KSAT", "San Antonio International", "San Antonio", "TX"),
]


# =============================================================================
# SIMULATED WORKLOADS
# =============================================================================


def simulate_io_bound(stationid: str, delay: float = 0.5) -> WeatherReport:
    """Simulate I/O-bound work (network request)."""
    time.sleep(delay)  # Simulate network latency
    return WeatherReport(stationid, 72.0, "Clear")


def simulate_cpu_bound(data_size: int = 100000) -> int:
    """Simulate CPU-bound work (computation)."""
    return sum(i * i for i in range(data_size))


async def simulate_io_bound_async(stationid: str, delay: float = 0.5) -> WeatherReport:
    """Async version of I/O-bound work."""
    await asyncio.sleep(delay)
    return WeatherReport(stationid, 72.0, "Clear")


# =============================================================================
# 1. THREADING EXAMPLES
# =============================================================================


def threading_basic_example() -> None:
    """Basic threading example."""
    print("\n  Basic Threading:")
    
    results = []
    lock = threading.Lock()
    
    def worker(stationid: str) -> None:
        report = simulate_io_bound(stationid)
        with lock:
            results.append(report)
    
    threads = []
    start = time.perf_counter()
    
    for airport in AIRPORTS[:4]:
        t = threading.Thread(target=worker, args=(airport.stationid,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    elapsed = time.perf_counter() - start
    print(f"    Fetched {len(results)} reports in {elapsed:.2f}s")
    print(f"    (Sequential would take ~{len(results) * 0.5:.1f}s)")


def threading_with_queue_example() -> None:
    """Threading with Queue for producer-consumer pattern."""
    print("\n  Threading with Queue:")
    
    task_queue: Queue = Queue()
    result_queue: Queue = Queue()
    
    def worker() -> None:
        while True:
            stationid = task_queue.get()
            if stationid is None:
                break
            report = simulate_io_bound(stationid, delay=0.2)
            result_queue.put(report)
            task_queue.task_done()
    
    # Start workers
    num_workers = 3
    threads = []
    for _ in range(num_workers):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    
    # Submit tasks
    start = time.perf_counter()
    for airport in AIRPORTS:
        task_queue.put(airport.stationid)
    
    # Wait for completion
    task_queue.join()
    
    # Stop workers
    for _ in range(num_workers):
        task_queue.put(None)
    for t in threads:
        t.join()
    
    elapsed = time.perf_counter() - start
    print(f"    Processed {result_queue.qsize()} items with {num_workers} workers")
    print(f"    Elapsed: {elapsed:.2f}s")


def threading_lock_example() -> None:
    """Thread synchronization with locks."""
    print("\n  Thread Synchronization:")
    
    class Counter:
        def __init__(self):
            self._value = 0
            self._lock = threading.Lock()
        
        def increment(self, amount: int = 1) -> None:
            with self._lock:
                self._value += amount
        
        @property
        def value(self) -> int:
            with self._lock:
                return self._value
    
    counter = Counter()
    
    def worker() -> None:
        for _ in range(1000):
            counter.increment()
    
    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"    Final counter value: {counter.value}")
    print(f"    Expected: 10000")


# =============================================================================
# 2. MULTIPROCESSING EXAMPLES
# =============================================================================


def _cpu_worker(n: int) -> int:
    """CPU-bound worker function (must be at module level for pickling)."""
    return sum(i * i for i in range(n))


def multiprocessing_pool_example() -> None:
    """Multiprocessing Pool for CPU-bound work."""
    print("\n  Multiprocessing Pool:")
    
    data_sizes = [500000] * 8
    
    # Sequential baseline
    start = time.perf_counter()
    sequential_results = [_cpu_worker(n) for n in data_sizes]
    sequential_time = time.perf_counter() - start
    
    # Parallel with Pool
    start = time.perf_counter()
    with multiprocessing.Pool(processes=4) as pool:
        parallel_results = pool.map(_cpu_worker, data_sizes)
    parallel_time = time.perf_counter() - start
    
    print(f"    Sequential: {sequential_time:.2f}s")
    print(f"    Parallel (4 processes): {parallel_time:.2f}s")
    print(f"    Speedup: {sequential_time / parallel_time:.1f}x")


# =============================================================================
# 3. CONCURRENT.FUTURES EXAMPLES
# =============================================================================


def threadpool_executor_example() -> None:
    """ThreadPoolExecutor for I/O-bound work."""
    print("\n  ThreadPoolExecutor:")
    
    start = time.perf_counter()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(simulate_io_bound, airport.stationid): airport
            for airport in AIRPORTS
        }
        
        results = []
        for future in as_completed(futures):
            airport = futures[future]
            try:
                report = future.result()
                results.append(report)
            except Exception as e:
                print(f"    {airport.stationid} failed: {e}")
    
    elapsed = time.perf_counter() - start
    print(f"    Fetched {len(results)} reports in {elapsed:.2f}s")


def processpool_executor_example() -> None:
    """ProcessPoolExecutor for CPU-bound work."""
    print("\n  ProcessPoolExecutor:")
    
    data_sizes = [500000] * 8
    
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(_cpu_worker, data_sizes))
    elapsed = time.perf_counter() - start
    
    print(f"    Computed {len(results)} results in {elapsed:.2f}s")


def executor_map_example() -> None:
    """Using executor.map() for ordered results."""
    print("\n  Executor map():")
    
    stationids = [a.stationid for a in AIRPORTS[:4]]
    
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        # map() returns results in order
        reports = list(executor.map(simulate_io_bound, stationids))
    elapsed = time.perf_counter() - start
    
    print(f"    Reports (in order): {[r.stationid for r in reports]}")
    print(f"    Elapsed: {elapsed:.2f}s")


def executor_error_handling_example() -> None:
    """Error handling with futures."""
    print("\n  Error Handling:")
    
    def flaky_fetch(stationid: str) -> WeatherReport:
        if stationid == "KDFW":
            raise ValueError(f"Failed to fetch {stationid}")
        time.sleep(0.2)
        return WeatherReport(stationid, 72.0, "Clear")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(flaky_fetch, a.stationid): a 
            for a in AIRPORTS[:4]
        }
        
        successes = 0
        failures = 0
        
        for future in as_completed(futures):
            airport = futures[future]
            try:
                result = future.result()
                successes += 1
            except Exception as e:
                failures += 1
                print(f"    {airport.stationid} failed: {e}")
    
    print(f"    Successes: {successes}, Failures: {failures}")


# =============================================================================
# 4. ASYNCIO EXAMPLES
# =============================================================================


async def asyncio_basic_example() -> None:
    """Basic asyncio example."""
    print("\n  Basic Asyncio:")
    
    start = time.perf_counter()
    
    # Concurrent execution with gather
    reports = await asyncio.gather(*[
        simulate_io_bound_async(a.stationid)
        for a in AIRPORTS
    ])
    
    elapsed = time.perf_counter() - start
    print(f"    Fetched {len(reports)} reports in {elapsed:.2f}s")
    print(f"    (Sequential would take ~{len(reports) * 0.5:.1f}s)")


async def asyncio_tasks_example() -> None:
    """Creating and managing tasks."""
    print("\n  Asyncio Tasks:")
    
    async def fetch_with_logging(stationid: str) -> WeatherReport:
        print(f"    Starting {stationid}...")
        report = await simulate_io_bound_async(stationid, delay=0.3)
        print(f"    Completed {stationid}")
        return report
    
    # Create tasks (start immediately)
    tasks = [
        asyncio.create_task(fetch_with_logging(a.stationid))
        for a in AIRPORTS[:3]
    ]
    
    # Wait for all
    results = await asyncio.gather(*tasks)
    print(f"    Got {len(results)} results")


async def asyncio_semaphore_example() -> None:
    """Rate limiting with semaphore."""
    print("\n  Asyncio Semaphore (rate limiting):")
    
    semaphore = asyncio.Semaphore(2)  # Max 2 concurrent
    
    async def limited_fetch(stationid: str) -> WeatherReport:
        async with semaphore:
            print(f"    Fetching {stationid}...")
            return await simulate_io_bound_async(stationid, delay=0.3)
    
    start = time.perf_counter()
    results = await asyncio.gather(*[
        limited_fetch(a.stationid) for a in AIRPORTS
    ])
    elapsed = time.perf_counter() - start
    
    print(f"    Fetched {len(results)} with max 2 concurrent")
    print(f"    Elapsed: {elapsed:.2f}s")


async def asyncio_timeout_example() -> None:
    """Timeout handling."""
    print("\n  Asyncio Timeout:")
    
    async def slow_operation() -> str:
        await asyncio.sleep(5)
        return "Done"
    
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=1.0)
        print(f"    Result: {result}")
    except asyncio.TimeoutError:
        print("    Operation timed out (as expected)")


async def asyncio_taskgroup_example() -> None:
    """TaskGroup for structured concurrency (Python 3.11+)."""
    print("\n  Asyncio TaskGroup:")
    
    async def fetch(stationid: str) -> WeatherReport:
        await asyncio.sleep(0.2)
        return WeatherReport(stationid, 72.0, "Clear")
    
    results = []
    async with asyncio.TaskGroup() as tg:
        for airport in AIRPORTS[:4]:
            task = tg.create_task(fetch(airport.stationid))
            # Can't easily collect results here, but all complete together
    
    print("    All tasks completed successfully")


async def run_async_examples() -> None:
    """Run all async examples."""
    await asyncio_basic_example()
    await asyncio_tasks_example()
    await asyncio_semaphore_example()
    await asyncio_timeout_example()
    await asyncio_taskgroup_example()


# =============================================================================
# 5. COMPARISON
# =============================================================================


def compare_approaches() -> None:
    """Compare different concurrency approaches."""
    print("\n  Approach Comparison (6 I/O tasks, 0.5s each):")
    
    stationids = [a.stationid for a in AIRPORTS]
    
    # Sequential
    start = time.perf_counter()
    for sid in stationids:
        simulate_io_bound(sid)
    sequential_time = time.perf_counter() - start
    
    # Threading
    start = time.perf_counter()
    threads = []
    for sid in stationids:
        t = threading.Thread(target=simulate_io_bound, args=(sid,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    threading_time = time.perf_counter() - start
    
    # ThreadPoolExecutor
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=6) as executor:
        list(executor.map(simulate_io_bound, stationids))
    executor_time = time.perf_counter() - start
    
    # Asyncio
    async def run_async():
        await asyncio.gather(*[
            simulate_io_bound_async(sid) for sid in stationids
        ])
    
    start = time.perf_counter()
    asyncio.run(run_async())
    asyncio_time = time.perf_counter() - start
    
    print(f"    Sequential:        {sequential_time:.2f}s")
    print(f"    Threading:         {threading_time:.2f}s")
    print(f"    ThreadPoolExecutor: {executor_time:.2f}s")
    print(f"    Asyncio:           {asyncio_time:.2f}s")


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """Run all concurrency demonstrations."""
    print("=" * 70)
    print("CONCURRENCY FUNDAMENTALS DEMONSTRATION")
    print("=" * 70)
    
    # Threading
    print("\n" + "=" * 70)
    print("1. THREADING")
    print("=" * 70)
    threading_basic_example()
    threading_with_queue_example()
    threading_lock_example()
    
    # Multiprocessing
    print("\n" + "=" * 70)
    print("2. MULTIPROCESSING")
    print("=" * 70)
    multiprocessing_pool_example()
    
    # concurrent.futures
    print("\n" + "=" * 70)
    print("3. CONCURRENT.FUTURES")
    print("=" * 70)
    threadpool_executor_example()
    processpool_executor_example()
    executor_map_example()
    executor_error_handling_example()
    
    # Asyncio
    print("\n" + "=" * 70)
    print("4. ASYNCIO")
    print("=" * 70)
    asyncio.run(run_async_examples())
    
    # Comparison
    print("\n" + "=" * 70)
    print("5. COMPARISON")
    print("=" * 70)
    compare_approaches()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
  | Approach           | Best For              | GIL Impact |
  |--------------------|----------------------|------------|
  | Threading          | I/O-bound tasks      | Releases   |
  | Multiprocessing    | CPU-bound tasks      | Bypasses   |
  | ThreadPoolExecutor | Simple I/O parallel  | Releases   |
  | ProcessPoolExecutor| Simple CPU parallel  | Bypasses   |
  | Asyncio            | Many concurrent I/O  | N/A        |
  
  Quick Guide:
  - Network/file I/O → asyncio or ThreadPoolExecutor
  - CPU computation → ProcessPoolExecutor
  - Mixed workload → Combine approaches
    """)
    
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
