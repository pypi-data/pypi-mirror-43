#!python3
#distutils: language = c++
import time
import math
import statistics
import random


__all__ = ("randint", "uniform", "distribution_timer")


cdef extern from "Pyewacket.hpp":
    double _generate_canonical          "Pyewacket::generate_canonical"()
    long long _random_int               "Pyewacket::random_int"(long long, long long)
    long long _random_range             "Pyewacket::random_range"(long long, long long, int)

    long long _random_binomial          "Pyewacket::random_binomial"(long long, double)
    long long _random_negative_binomial "Pyewacket::random_negative_binomial"(long long, double)
    long long _random_geometric         "Pyewacket::random_geometric"(double)
    long long _random_poisson           "Pyewacket::random_poisson"(double)
    long long _random_discrete          "Pyewacket::random_discrete"(long long, double, double)
    double _random_float                "Pyewacket::random_float"(double, double)
    double _random_exponential          "Pyewacket::random_exponential"(double)
    double _random_gamma                "Pyewacket::random_gamma"(double, double)
    double _random_weibull              "Pyewacket::random_weibull"(double, double)
    double _random_extreme_value        "Pyewacket::random_extreme_value"(double, double)
    double _random_normal               "Pyewacket::random_normal"(double, double)
    double _random_log_normal           "Pyewacket::random_log_normal"(double, double)
    double _random_chi_squared          "Pyewacket::random_chi_squared"(double)
    double _random_cauchy               "Pyewacket::random_cauchy"(double, double)
    double _random_fisher_f             "Pyewacket::random_fisher_f"(double, double)
    double _random_student_t            "Pyewacket::random_student_t"(double)


# RANDOM VALUE #
def random_value(arr):
    size = len(arr)
    return arr[_random_int(0, size-1)]


def cumulative_weighted_choice(table):
    max_weight = table[-1][0]
    rand = _random_int(0, max_weight-1)
    for weight, value in table:
        if weight > rand:
            return value


# RANDOM INTEGER #
def randint(a, b) -> int:
    return _random_int(a, b)

def randrange(start, stop=0, step=1):
    return _random_range(start, stop, step)


def random_binomial(number_of_trials = 10, probability = 0.5) -> int:
    return _random_binomial(number_of_trials, probability)

def random_negative_binomial(number_of_trials = 1, probability = 0.5) -> int:
    return _random_negative_binomial(number_of_trials, probability)

def random_geometric(probability = 0.5) -> int:
    return _random_geometric(probability)

def random_poisson(mean = math.pi) -> int:
    return _random_poisson(mean)

def random_discrete(count = 7, xmin = 1, xmax = 30) -> int:
    return _random_discrete(count, xmin, xmax)


# RANDOM FLOATING POINT #
def random():
    return _generate_canonical()

def uniform(a, b) -> float:
    return _random_float(a, b)

def random_exponential(lambda_rate = 1.0) -> float:
    return _random_exponential(lambda_rate)

def random_gamma(shape = 1.0, scale = 1.0) -> float:
    return _random_gamma(shape, scale)

def random_weibull(shape = 1.0, scale = 1.0) -> float:
    return _random_weibull(shape, scale)

def random_extreme_value(location = 0.0, scale = 1.0) -> float:
    return _random_extreme_value(location, scale)

def random_normal(mean = 5.0, std_dev = 2.0) -> float:
    return _random_normal(mean, std_dev)

def random_log_normal(log_mean = 1.6, log_deviation = 0.25) -> float:
    return _random_log_normal(log_mean, log_deviation)

def random_chi_squared(degrees_of_freedom = 1.0) -> float:
    return _random_chi_squared(degrees_of_freedom)

def random_cauchy(location = 0.0, scale = 1.0) -> float:
    return _random_cauchy(location, scale)

def random_fisher_f(degrees_of_freedom_1 = 8.0, degrees_of_freedom_2 = 8.0) -> float:
    return _random_fisher_f(degrees_of_freedom_1, degrees_of_freedom_2)

def random_student_t(degrees_of_freedom = 8.0) -> float:
    return _random_student_t(degrees_of_freedom)


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


def distribution_timer(func: staticmethod, *args, num_cycles=100000, label="", post_processor=None, **kwargs):
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
