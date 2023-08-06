#pragma once
#include <random>
#include <algorithm>


namespace RNG {
using Integer = long long;
using Float = long double;
static std::random_device hardware_seed;
static std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 10>, 256> generator { hardware_seed() };


/// UTILITIES ///
template <typename Function, typename Number>
Number analytic_continuation(Function func, Number num) {
    if (num < 0) return -func(-num);
    else if (num == 0) return 0;
    else return func(num);
}

Float probability_clamp(Float probability) {
    return std::clamp(probability, Float(0.0), Float(1.0));
}

Integer counting_clamp(Integer target) {
    return std::max(target, Integer(1));
}

Float weight_clamp(Float target) {
    return std::max(target, Float(0.0));
}


/// BINARY ///
bool random_bool(Float truth_factor) {
    std::bernoulli_distribution distribution(probability_clamp(truth_factor));
    return distribution(generator);
}

/// INTEGER ///
Integer random_int(Integer left_limit, Integer right_limit) {
    std::uniform_int_distribution<Integer> distribution {
        std::min(left_limit, right_limit),
        std::max(right_limit, left_limit)
    };
    return distribution(generator);
}

Integer random_binomial(Integer number_of_trials, Float probability) {
    std::binomial_distribution<Integer> distribution(
        counting_clamp(number_of_trials),
        probability_clamp(probability)
    );
    return distribution(generator);
}

Integer random_negative_binomial(Integer number_of_trials, Float probability) {
    std::negative_binomial_distribution<Integer> distribution(
        counting_clamp(number_of_trials),
        probability_clamp(probability)
    );
    return distribution(generator);
}

Integer random_geometric(Float probability) {
    std::geometric_distribution<Integer> distribution(
        probability_clamp(probability)
    );
    return distribution(generator);
}

Integer random_poisson(Float mean) {
    std::poisson_distribution<Integer> distribution(mean);
    return distribution(generator);
}

Integer random_discrete(Integer count, Float xmin, Float xmax, Integer step) {
    std::discrete_distribution<Integer> distribution(
        counting_clamp(count),
        weight_clamp(xmin),
        weight_clamp(xmax),
        [step](auto x) { return x + counting_clamp(step); }
    );
    return distribution(generator);
}

/// FLOAT ///
Float generate_canonical() {
    return std::generate_canonical<Float, std::numeric_limits<Float>::digits10>(generator);
}

Float random_float(Float left_limit, Float right_limit) {
    std::uniform_real_distribution<Float> distribution{
        std::min(left_limit, right_limit),
        std::max(right_limit, left_limit)
    };
    return distribution(generator);
}

Float random_exponential(Float lambda_rate) {
    std::exponential_distribution<Float> distribution(
        weight_clamp(lambda_rate)
    );
    return distribution(generator);
}

Float random_gamma(Float shape, Float scale) {
    std::gamma_distribution<Float> distribution(shape, scale);
    return distribution(generator);
}

Float random_weibull(Float shape, Float scale) {
    std::weibull_distribution<Float> distribution(shape, scale);
    return distribution(generator);
}

Float random_extreme_value(Float location, Float scale) {
    std::extreme_value_distribution<Float> distribution(location, scale);
    return distribution(generator);
}

Float random_normal(Float mean, Float std_dev) {
    std::normal_distribution<Float> distribution(mean, std_dev);
    return distribution(generator);
}

Float random_log_normal(Float log_mean, Float log_deviation) {
    std::lognormal_distribution<Float> distribution(log_mean, log_deviation);
    return distribution(generator);
}

Float random_chi_squared(Float degrees_of_freedom) {
    std::chi_squared_distribution<Float> distribution(
        weight_clamp(degrees_of_freedom)
    );
    return distribution(generator);
}

Float random_cauchy(Float location, Float scale) {
    std::cauchy_distribution<Float> distribution(location, scale);
    return distribution(generator);
}

Float random_fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) {
    std::fisher_f_distribution<Float> distribution(
        weight_clamp(degrees_of_freedom_1),
        weight_clamp(degrees_of_freedom_2)
    );
    return distribution(generator);
}

Float random_student_t(Float degrees_of_freedom) {
    std::student_t_distribution<Float> distribution(
        weight_clamp(degrees_of_freedom)
    );
    return distribution(generator);
}

} // end RNG namespace
