import time
import statistics
from Query import rewrite_query, get_merged_answers, get_merged_answers_reWrite

RUNS = 30

def bench(fn):
    times = []
    last = None
    for _ in range(RUNS):
        t0 = time.perf_counter()
        last = fn()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)  # ms
    return {
        "mean": statistics.mean(times),
        "p50": statistics.median(times),
        "p95": sorted(times)[int(0.95 * (RUNS - 1))],
        "last": last
    }

QUERY = "Who can use swords in this game?"

# -------------------------
# A) Rewrite only
# -------------------------
def run_rewrite():
    return rewrite_query(QUERY)

# -------------------------
# B) Retrieval only (no rewrite)
# -------------------------
def run_no_rewrite():
    return get_merged_answers(QUERY)

# -------------------------
# C) Rewrite + Retrieval
# -------------------------
def run_with_rewrite():
    rq = rewrite_query(QUERY)
    return get_merged_answers_reWrite(rq)

# -------------------------
# Run benches
# -------------------------
rewrite_stats = bench(run_rewrite)
no_rw_stats = bench(run_no_rewrite)
with_rw_stats = bench(run_with_rewrite)

print("\n=== Rewrite Latency (ms) ===")
print(f"mean={rewrite_stats['mean']:.2f}  p50={rewrite_stats['p50']:.2f}  p95={rewrite_stats['p95']:.2f}")

print("\n=== Retrieval WITHOUT rewrite (ms) ===")
print(f"mean={no_rw_stats['mean']:.2f}  p50={no_rw_stats['p50']:.2f}  p95={no_rw_stats['p95']:.2f}")

print("\n=== Retrieval WITH rewrite (ms) ===")
print(f"mean={with_rw_stats['mean']:.2f}  p50={with_rw_stats['p50']:.2f}  p95={with_rw_stats['p95']:.2f}")

print("\n=== Overhead of rewrite (approx) ===")
print(f"{with_rw_stats['mean'] - no_rw_stats['mean']:.2f} ms")
