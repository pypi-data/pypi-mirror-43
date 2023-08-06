#!python3
#distutils: language = c++
import time
import statistics
import itertools


cdef extern from "Pyewacket.hpp":
    double _generate_canonical          "Pyewacket::generate_canonical"()
    long long _random_below             "Pyewacket::random_below"(long long)
    long long _random_int               "Pyewacket::random_int"(long long, long long)
    long long _randrange                "Pyewacket::randrange"(long long, long long, int)
    double _random_float                "Pyewacket::random_float"(double, double)


# RANDOM VALUE #
def choice(seq):
    size = len(seq)
    if size == 0:
        return None
    return seq[_random_below(size)]

def shuffle(x):
    size = len(x)
    for i in range(1, size):
        j = _random_int(0, i)
        x[i], x[j] = x[j], x[i]

def _cumulative_weighted_choice(pop, weights):
    max_weight = weights[-1]
    rand = _random_below(max_weight)
    for weight, value in zip(weights, pop):
        if weight > rand:
            return value

def choices(population, weights=None, *, cum_weights=None, k=1):
    if not weights and not cum_weights:
        return [choice(population) for _ in range(k)]
    if not cum_weights:
        cum_weights = list(itertools.accumulate(weights))
    assert len(cum_weights) == len(population), "The number of weights does not match the population"
    return [_cumulative_weighted_choice(population, cum_weights) for _ in range(k)]


# RANDOM INTEGER #
def randbelow(a) -> int:
    return _random_below(a)

def randint(a, b) -> int:
    return _random_int(a, b)

def randrange(start, stop=None, step=None):
    if not step:
        if not stop:
            return _random_below(start)
        else:
            return start + _random_below(stop - start)
    return _randrange(start, stop, step)


# RANDOM FLOATING POINT #
def random():
    return _generate_canonical()

def uniform(a, b) -> float:
    return _random_float(a, b)


# DISTRIBUTION & PERFORMANCE TEST SUITE #
def timer(func: staticmethod, *args, **kwargs):
    results = []
    outer_cycles = 32
    inner_cycles = 32
    for _ in range(outer_cycles):
        start = time.time_ns()
        for _ in range(inner_cycles):
            func(*args, **kwargs)
        end = time.time_ns()
        results.append((end - start) // inner_cycles)
    output = (
        f"Min: {min(results)}ns",
        f"Mid: {int(statistics.median(results))}ns",
        f"Max: {max(results)}ns",
    )
    print(f"Approximate Single Execution Time: {', '.join(output)}")


def distribution(func: staticmethod, *args, num_cycles, post_processor=None, **kwargs):
    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    print(f"Test Samples: {num_cycles}")
    ave = statistics.mean(results)
    median_lo = statistics.median_low(results)
    median_hi = statistics.median_high(results)
    median = median_lo if median_lo == median_hi else (median_lo, median_hi)
    std_dev = statistics.stdev(results, ave)
    output = (
        f" Minimum: {min(results)}",
        f" Median: {median}",
        f" Maximum: {max(results)}",
        f" Mean: {ave}",
        f" Std Deviation: {std_dev}",
    )
    if post_processor is None:
        print("Sample Statistics:")
        print("\n".join(output))
        processed_results = results
        unique_results = list(set(results))
        print(f"Sample Distribution:")
    else:
        print("Pre-processor Statistics:")
        print("\n".join(output))
        processed_results = list(map(post_processor, results))
        unique_results = list(set(processed_results))
        print(f"Post-processor Distribution using {post_processor.__name__} method:")
    unique_results.sort()
    result_obj = {
        key: f"{processed_results.count(key) / (num_cycles / 100)}%" for key in unique_results
    }
    for key, val in result_obj.items():
        print(f" {key}: {val}")


def distribution_timer(func: staticmethod, *args, num_cycles=10000, label="", post_processor=None, **kwargs):
    def samples(func, *args, **kwargs):
        return f', '.join(str(func(*args, **kwargs)) for _ in range(5))

    arguments = ', '.join([str(v) for v in args] + [f'{k}={v}' for k, v in kwargs.items()])
    if label:
        print(f"Output Analysis: {label}({arguments})")
    elif hasattr(func, "__qualname__"):
        print(f"Output Distribution: {func.__qualname__}({arguments})")
    elif hasattr(func, "__name__"):
        print(f"Output Distribution: {func.__name__}({arguments})")
    else:
        print(f"Output Analysis: {func}({arguments})")
    timer(func, *args, **kwargs)
    print(f"Raw Samples: {samples(func, *args, **kwargs)}")
    distribution(func, *args, num_cycles=num_cycles, post_processor=post_processor, **kwargs)
    print("")
