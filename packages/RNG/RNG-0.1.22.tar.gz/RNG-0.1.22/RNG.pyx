#!python3
#distutils: language = c++
import time
import math
import statistics
import random


cdef extern from "RNG.hpp":
    long long _vortex_random_below "RNG::vortex_random_below"(long long)
    long long _min_int "RNG::min_int"()
    long long _max_int "RNG::max_int"()
    double _min_float "RNG::min_float"()
    double _max_float "RNG::max_float"()
    double _min_below_zero "RNG::min_below_zero"()
    double _min_above_zero "RNG::min_above_zero"()
    int _random_bool "RNG::random_bool"(double)
    long long _random_int "RNG::random_int"(long long, long long)
    long long _random_below "RNG::random_below"(long long)
    long long _random_binomial "RNG::random_binomial"(long long, double)
    long long _random_negative_binomial "RNG::random_negative_binomial"(long long, double)
    long long _random_geometric "RNG::random_geometric"(double)
    long long _random_poisson "RNG::random_poisson"(double)
    long long _random_discrete "RNG::random_discrete"(long long, double, double)
    double _generate_canonical "RNG::generate_canonical"()
    double _random_float "RNG::random_float"(double, double)
    double _random_exponential "RNG::random_exponential"(double)
    double _random_gamma "RNG::random_gamma"(double, double)
    double _random_weibull "RNG::random_weibull"(double, double)
    double _random_extreme_value "RNG::random_extreme_value"(double, double)
    double _random_normal "RNG::random_normal"(double, double)
    double _random_log_normal "RNG::random_log_normal"(double, double)
    double _random_chi_squared "RNG::random_chi_squared"(double)
    double _random_cauchy "RNG::random_cauchy"(double, double)
    double _random_fisher_f "RNG::random_fisher_f"(double, double)
    double _random_student_t "RNG::random_student_t"(double)


# EXPERIMENTAL VORTEX ENGINE #
def vortex_random_below(upper_bound = 10) -> int:
    return _vortex_random_below(upper_bound)


# RANDOM BOOLEAN #
def random_bool(truth_factor = 0.5) -> bool:
    return _random_bool(truth_factor) == 1


# RANDOM INTEGER #
def random_int(left_limit = 1, right_limit = 20) -> int:
    return _random_int(left_limit, right_limit)

def random_below(upper_bound = 10) -> int:
    return _random_below(upper_bound)

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
def generate_canonical():
    return _generate_canonical()

def random_float(left_limit = 0.0, right_limit = 1.0) -> float:
    return _random_float(left_limit, right_limit)
    
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


def quick_test(n=10000):
    def floor_mod_10(x):
        return math.floor(x) % 10

    print("\nQuick Test: RNG Storm Engine")
    start = time.time()
    print(f" Min Integer: {_min_int()}")
    print(f" Max Integer:  {_max_int()}")
    print(f" Min Float: {_min_float()}")
    print(f" Max Float:  {_max_float()}")
    print(f" Min Below Zero: {_min_below_zero()}")
    print(f" Min Above Zero:  {_min_above_zero()}")
    print("\n\nBinary Tests\n")
    distribution_timer(
        random_bool, truth_factor=1/3,
        num_cycles=n)
    print("\nInteger Tests\n")
    print("Base Case for random_int:")
    distribution_timer(
        random.randint, a=1, b=6,
        num_cycles=n
    )
    distribution_timer(
        random_int, left_limit=1, right_limit=6,
        num_cycles=n
    )
    print("Typhoon Engine:")
    distribution_timer(
        random_below, upper_bound=6,
        num_cycles=n
    )
    distribution_timer(
        random_binomial, number_of_trials=4, probability=0.5,
        num_cycles=n
    )
    distribution_timer(
        random_negative_binomial, number_of_trials=5, probability=0.75,
        num_cycles=n
    )
    distribution_timer(
        random_geometric, probability=0.75,
        num_cycles=n
    )
    distribution_timer(
        random_poisson, mean=4.5,
        num_cycles=n
    )
    distribution_timer(
        random_discrete, count=7, xmin=1, xmax=30,
        num_cycles=n
    )
    print("\nFloating Point Tests\n")
    print("Base Case for generate_canonical:")
    distribution_timer(
        random.random,
        num_cycles=n, post_processor=round
    )
    distribution_timer(
        generate_canonical,
        num_cycles=n, post_processor=round
    )
    distribution_timer(
        random_float, left_limit=0.0, right_limit=10.0,
        num_cycles=n, post_processor=math.ceil
    )
    print("Base Case for random_exponential:")
    distribution_timer(
        random.expovariate, lambd=1.0,
        num_cycles=n, post_processor=floor_mod_10
    )
    distribution_timer(
        random_exponential, lambda_rate=1.0,
        num_cycles=n, post_processor=floor_mod_10
    )
    print("Base Case for random_gamma:")
    distribution_timer(
        random.gammavariate, alpha=1.0, beta=1.0,
        num_cycles=n, post_processor=floor_mod_10
    )
    distribution_timer(
        random_gamma, shape=1.0, scale=1.0,
        num_cycles=n, post_processor=floor_mod_10
    )
    distribution_timer(
        random_weibull, shape=1.0, scale=1.0,
        num_cycles=n, post_processor=floor_mod_10
    )
    distribution_timer(
        random_extreme_value, location=0.0, scale=1.0,
        num_cycles=n, post_processor=round
    )
    print("Base Case for random_normal:")
    distribution_timer(
        random.gauss, mu=5.0, sigma=2.0,
        num_cycles=n, post_processor=round
    )
    distribution_timer(
        random_normal, mean=5.0, std_dev=2.0,
        num_cycles=n, post_processor=round
    )
    print("Base Case for random_log_normal:")
    distribution_timer(
        random.lognormvariate, mu=1.6, sigma=0.25,
        num_cycles=n, post_processor=round
    )
    distribution_timer(
        random_log_normal, log_mean=1.6, log_deviation=0.25,
        num_cycles=n, post_processor=round
    )
    distribution_timer(
        random_chi_squared, degrees_of_freedom=1.0,
        num_cycles=n, post_processor=floor_mod_10
    )
    distribution_timer(
        random_cauchy, location=0.0, scale=1.0,
        num_cycles=n, post_processor=floor_mod_10
    )
    distribution_timer(
        random_fisher_f, degrees_of_freedom_1=8.0, degrees_of_freedom_2=8.0,
        num_cycles=n, post_processor=floor_mod_10
    )
    distribution_timer(
        random_student_t, degrees_of_freedom=8.0,
        num_cycles=n, post_processor=round
    )
    end = time.time()
    duration = round(end - start, 4)
    print()
    print('=' * 73)
    print(f"Total Test Time: {duration} seconds\n\n")

    print("Experimental, RNG Vortex Engine:")
    distribution_timer(vortex_random_below, 10, num_cycles=n)
    print("Base Case 1, RNG Storm Engine:")
    distribution_timer(random_below, 10, num_cycles=n)
    print("Base Case 2, Random.py Engine:")
    distribution_timer(random.randrange, 10, num_cycles=n)
