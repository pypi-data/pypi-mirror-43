# RNG: Random Number Generator

### Provides low-level access to the C++ Random library.

### Random Engine
Mersenne Twister 64. More info: https://en.wikipedia.org/wiki/Mersenne_Twister.


##### Random Bool
- random_bool(percent_true: float) -> bool


#### Random Integer
- random_int(lo_limit: int, hi_limit: int) -> int
- random_binomial(number_of_trials: int, probability: float) -> int
- random_negative_binomial(number_of_trials: int, probability: float) -> int
- random_geometric(probability: float) -> int
- random_poisson(average: float) -> int
- random_discrete(count: int, xmin: int, xmax: int) -> int


#### Random Floating Point
- random_floating_point(lo_limit: float, hi_limit: float) -> float
- random_exponential(lambda_rate: float) -> float
- random_gamma(shape: float, scale: float) -> float
- random_weibull(shape: float, scale: float) -> float
- random_extreme_value(shape: float, scale: float) -> float
- random_normal(average: float, std_dev: float) -> float
- random_log_normal(log_mean: float, log_deviation: float) -> float
- random_chi_squared(degrees_of_freedom: float) -> float
- random_cauchy(location: float, scale: float) -> float
- random_fisher_f(degrees_of_freedom_1: float, degrees_of_freedom_2: float) -> float
- random_student_t(degrees_of_freedom: float) -> float


#### C-style Random
- c_rand() -> int
