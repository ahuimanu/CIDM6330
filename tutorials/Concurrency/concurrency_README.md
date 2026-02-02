# Concurrency Fundamentals in Python

Concurrency enables programs to handle multiple tasks efficiently. Python offers three main approaches: threading, multiprocessing, and asyncio. Understanding when to use each is essential for building scalable systems.

## Table of Contents

1. [Concurrency vs Parallelism](#concurrency-vs-parallelism)
2. [The GIL](#the-gil)
3. [Threading](#threading)
4. [Multiprocessing](#multiprocessing)
5. [concurrent.futures](#concurrentfutures)
6. [Asyncio](#asyncio)
7. [Choosing the Right Approach](#choosing-the-right-approach)
8. [Best Practices](#best-practices)

---

## Concurrency vs Parallelism

**Concurrency**: Managing multiple tasks that can make progress over time (interleaving).

**Parallelism**: Executing multiple tasks simultaneously on multiple CPU cores.

| Scenario | Concurrency | Parallelism |
|----------|-------------|-------------|
| I/O waiting | ✓ | Not needed |
| CPU computation | Limited by GIL | ✓ (multiprocessing) |

---

## The GIL

The Global Interpreter Lock prevents multiple threads from executing Python bytecode simultaneously.

**Key implications:**
- Threading does NOT speed up CPU-bound work
- Threading DOES help I/O-bound work (GIL releases during I/O)
- Multiprocessing bypasses the GIL (separate interpreters)

```python
# CPU-bound: Use multiprocessing, not threading
# I/O-bound: Threading or asyncio work well
```

---

## Threading

Threads share memory within a process. Good for I/O-bound tasks.

```python
import threading
import time

def fetch_weather(stationid: str) -> None:
    print(f"Fetching {stationid}...")
    time.sleep(1)  # Simulate I/O
    print(f"Done: {stationid}")

# Create and start threads
threads = []
for sid in ["KAMA", "KLBB", "KMAF"]:
    t = threading.Thread(target=fetch_weather, args=(sid,))
    threads.append(t)
    t.start()

# Wait for completion
for t in threads:
    t.join()
```

### Thread Synchronization

```python
import threading

class Counter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1
```

---

## Multiprocessing

Processes run in separate memory spaces. Good for CPU-bound tasks.

```python
import multiprocessing

def compute(data: list) -> int:
    return sum(x * x for x in data)

if __name__ == "__main__":
    with multiprocessing.Pool(4) as pool:
        results = pool.map(compute, [range(1000) for _ in range(10)])
```

---

## concurrent.futures

High-level interface for both threading and multiprocessing.

### ThreadPoolExecutor (I/O-bound)

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_weather(stationid: str) -> dict:
    # Simulate I/O
    return {"stationid": stationid, "temp": 72}

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(fetch_weather, sid): sid
               for sid in ["KAMA", "KLBB", "KMAF"]}

    for future in as_completed(futures):
        result = future.result()
        print(f"{result['stationid']}: {result['temp']}°F")
```

### ProcessPoolExecutor (CPU-bound)

```python
from concurrent.futures import ProcessPoolExecutor

def compute(n: int) -> int:
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(compute, [10**6] * 10))
```

---

## Asyncio

Single-threaded cooperative multitasking. Excellent for many concurrent I/O operations.

### Basic Async/Await

```python
import asyncio

async def fetch_weather(stationid: str) -> dict:
    print(f"Fetching {stationid}...")
    await asyncio.sleep(1)  # Non-blocking
    return {"stationid": stationid, "temp": 72}

async def main():
    # Concurrent execution
    results = await asyncio.gather(
        fetch_weather("KAMA"),
        fetch_weather("KLBB"),
        fetch_weather("KMAF"),
    )
    print(results)

asyncio.run(main())
```

### Rate Limiting with Semaphore

```python
import asyncio

async def fetch(stationid: str, sem: asyncio.Semaphore) -> dict:
    async with sem:  # Limit concurrency
        await asyncio.sleep(0.5)
        return {"stationid": stationid}

async def main():
    sem = asyncio.Semaphore(3)  # Max 3 concurrent
    tasks = [fetch(f"K{i}", sem) for i in range(10)]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```

### Timeout

```python
import asyncio

async def slow_operation():
    await asyncio.sleep(10)

async def main():
    try:
        await asyncio.wait_for(slow_operation(), timeout=2.0)
    except asyncio.TimeoutError:
        print("Timed out!")

asyncio.run(main())
```

---

## Choosing the Right Approach

| Workload | Best Choice |
|----------|-------------|
| Many network requests | asyncio |
| File I/O | threading |
| Database queries | asyncio or threading |
| CPU computation | multiprocessing |
| Simple parallelism | concurrent.futures |

**Rule of thumb:**
- I/O-bound → asyncio or threading
- CPU-bound → multiprocessing

---

## Best Practices

1. **Limit concurrency** - Don't overwhelm resources
2. **Handle exceptions** - Use try/except in workers
3. **Use context managers** - Proper cleanup
4. **Avoid shared mutable state** - Return values instead
5. **Profile first** - Measure before optimizing

```python
# Good pattern
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(task, arg): arg for arg in args}
    for future in as_completed(futures):
        try:
            result = future.result()
        except Exception as e:
            print(f"Failed: {e}")
```

---

## Further Reading

- [threading documentation](https://docs.python.org/3/library/threading.html)
- [multiprocessing documentation](https://docs.python.org/3/library/multiprocessing.html)
- [concurrent.futures documentation](https://docs.python.org/3/library/concurrent.futures.html)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
