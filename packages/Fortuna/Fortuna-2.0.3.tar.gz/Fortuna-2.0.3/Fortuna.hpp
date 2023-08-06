#pragma once
#include <cstdlib>
#include <cmath>
#include <random>
#include <vector>
#include <algorithm>


namespace Fortuna {
using Integer = long long;
using Float = double;
using Bool = bool;
static std::random_device hardware_seed;
static const int Block_shuffle { 256 };
static const int Pre_drop { 12 };
static const int Post_drop { 10 };
static std::mt19937 twister { hardware_seed() };
static std::mt19937_64 cyclone { hardware_seed() };
static std::shuffle_order_engine<std::mt19937_64, Block_shuffle> hurricane { hardware_seed() };
static std::discard_block_engine<std::mt19937_64, Pre_drop, Post_drop> tornado { hardware_seed() };
static std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, Pre_drop, Post_drop>, Block_shuffle> typhoon { hardware_seed() };

template <typename Number>
auto smart_clamp(Number target, Number left_limit, Number right_limit) {
    return std::clamp(target, std::min(left_limit, right_limit), std::max(right_limit, left_limit));
}

template <typename S>
auto vortex(S storm) {
    static struct GearBox {
        const int gear;
        GearBox(int gear) : gear(gear) { std::srand(hardware_seed()); }
        int operator()() const { return std::rand() % gear; }
    } gear_box(5);
    const int fate = smart_clamp(gear_box(), gear_box(), gear_box());
    if (fate == 3 ) return storm(twister);
    if (fate == 2 ) return storm(hurricane);
    if (fate == 1 ) return storm(cyclone);
    if (fate == 0 ) return storm(tornado);
    return storm(typhoon);
}

template <typename Function, typename Number>
auto analytic_continuation(Function && func, Number number) {
    const Number minimum { -std::numeric_limits<Number>::max() };
    const Number maximum { std::numeric_limits<Number>::max() };
    const Number num { smart_clamp(number, minimum, maximum) };
    if (num < 0) return -func(-num);
    if (num == 0) return Number(0);
    return func(num);
}

Float generate_canonical() {
    return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(hurricane);
}

Bool random_bool(Float truth_factor) {
    std::bernoulli_distribution distribution {
        smart_clamp(truth_factor, 0.0, 1.0)
    };
    return distribution(hurricane);
}

Integer vortex_random_below(Integer upper_bound) {
    if (upper_bound > 0) {
        std::uniform_int_distribution<Integer> distribution { 0, upper_bound - 1 };
        return vortex(distribution);
    } else return analytic_continuation(vortex_random_below, upper_bound);
}

Integer random_int(Integer left_limit, Integer right_limit) {
    std::uniform_int_distribution<Integer> distribution {
        std::min(left_limit, right_limit),
        std::max(right_limit, left_limit)
    };
    return distribution(hurricane);
}

Integer random_binomial(Integer number_of_trials, Float probability) {
    std::binomial_distribution<Integer> distribution {
        std::max(number_of_trials, Integer(1)),
        smart_clamp(probability, 0.0, 1.0)
    };
    return distribution(hurricane);
}

Integer random_negative_binomial(Integer number_of_trials, Float probability) {
    std::negative_binomial_distribution<Integer> distribution {
        std::max(number_of_trials, Integer(1)),
        smart_clamp(probability, 0.0, 1.0)
    };
    return distribution(hurricane);
}

Integer random_geometric(Float probability) {
    std::geometric_distribution<Integer> distribution {
        smart_clamp(probability, 0.0, 1.0)
    };
    return distribution(hurricane);
}

Integer random_poisson(Float mean) {
    std::poisson_distribution<Integer> distribution {
        mean
    };
    return distribution(hurricane);
}

Integer random_discrete(size_t count, Float xmin, Float xmax) {
    std::discrete_distribution<Integer> distribution {
        count,
        std::max(xmin, 0.0),
        std::max(xmax, 0.0),
        [](auto x) { return x + 1; }
    };
    return distribution(hurricane);
}

Float random_float(Float left_limit, Float right_limit) {
    std::uniform_real_distribution<Float> distribution {
        std::min(left_limit, right_limit),
        std::max(right_limit, left_limit)
    };
    return distribution(hurricane);
}

Float random_exponential(Float lambda_rate) {
    std::exponential_distribution<Float> distribution {
        lambda_rate
    };
    return distribution(hurricane);
}

Float random_gamma(Float shape, Float scale) {
    std::gamma_distribution<Float> distribution {
        shape,
        scale
    };
    return distribution(hurricane);
}

Float random_weibull(Float shape, Float scale) {
    std::weibull_distribution<Float> distribution {
        shape,
        scale
    };
    return distribution(hurricane);
}

Float random_extreme_value(Float location, Float scale) {
    std::extreme_value_distribution<Float> distribution {
        location,
        scale
    };
    return distribution(hurricane);
}

Float random_normal(Float mean, Float std_dev) {
    std::normal_distribution<Float> distribution {
        mean,
        std_dev
    };
    return distribution(hurricane);
}

Float random_log_normal(Float log_mean, Float log_deviation) {
    std::lognormal_distribution<Float> distribution {
        log_mean,
        log_deviation
    };
    return distribution(hurricane);
}

Float random_chi_squared(Float degrees_of_freedom) {
    std::chi_squared_distribution<Float> distribution {
        std::max(degrees_of_freedom, Float(0.0))
    };
    return distribution(hurricane);
}

Float random_cauchy(Float location, Float scale) {
    std::cauchy_distribution<Float> distribution {
        location,
        scale
    };
    return distribution(hurricane);
}

Float random_fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) {
    std::fisher_f_distribution<Float> distribution {
        std::max(degrees_of_freedom_1, Float(0.0)),
        std::max(degrees_of_freedom_2, Float(0.0))
    };
    return distribution(hurricane);
}

Float random_student_t(Float degrees_of_freedom) {
    std::student_t_distribution<Float> distribution {
        std::max(degrees_of_freedom, Float(0.0))
    };
    return distribution(hurricane);
}

Integer min_int() {
    return -std::numeric_limits<Integer>::max();
}

Integer max_int() {
    return std::numeric_limits<Integer>::max();
}

Float min_float() {
    return -std::numeric_limits<Float>::max();
}

Float max_float() {
    return std::numeric_limits<Float>::max();
}

Float min_below_zero() {
    return std::nextafter(0.0, std::numeric_limits<Float>::lowest());
}

Float min_above_zero() {
    return std::nextafter(0.0, std::numeric_limits<Float>::max());
}

/// Fortuna Special Functions
Integer random_below(Integer number) {
    if (number > 0) {
        std::uniform_int_distribution<Integer> distribution { 0, number - 1 };
        return distribution(hurricane);
    } else return analytic_continuation(random_below, number);
}

Integer random_range(Integer left_limit, Integer right_limit, int step) {
    auto step_by = std::abs(step);
    if (step_by > 1) {
        const Integer width = std::max(left_limit, right_limit) - std::min(left_limit, right_limit);
        if (step > 0) return std::min(left_limit, right_limit) + step_by * random_below((width + step_by) / step_by);
        else return std::max(left_limit, right_limit) - step_by * random_below((width + step_by) / step_by);
    }
    else if (step_by == 1) {
        return random_int(left_limit, right_limit);
    }
    else return left_limit;
}

Integer x_or_rand_below_y(Integer target, Integer upper_bound) {
    if (target >= 0 and target < upper_bound) return target;
    else return random_below(upper_bound);
}

Integer d(Integer sides) {
    if (sides > 0) {
        return random_int(1, sides);
    } else return analytic_continuation(d, sides);
}

Integer dice(Integer rolls, Integer sides) {
    if (rolls > 0) {
        Integer total = 0;
        for (auto i {0}; i < rolls; ++i) total += d(sides);
        return total;
    }
    if (rolls == 0) return 0;
    return -dice(-rolls, sides);
}

Integer ability_dice(Integer num) {
    const Integer n { smart_clamp(num, Integer(3), Integer(9)) };
    if (n == 3) return dice(3, 6);
    std::vector<Integer> theRolls(n);
    std::generate(begin(theRolls), end(theRolls), []() { return d(6); });
    std::partial_sort(begin(theRolls), begin(theRolls) + 3, end(theRolls), std::greater<Integer>());
    return std::accumulate(begin(theRolls), begin(theRolls) + 3, 0);
}

Integer plus_or_minus(Integer number) {
    return random_int(-number, number);
}

Integer plus_or_minus_linear(Integer number) {
    const Integer num { std::abs(number) };
    return dice(2, num + 1) - (num + 2);
}

Bool percent_true(Float truth_factor) {
    return random_float(0.0, 100.0) < truth_factor;
}

/// QM
Integer front_gauss(Integer number) {
    if (number > 0) { // Narrowing Float -> Integer
        const Integer result { Integer(std::floor(random_gamma(1.0, number / 10.0))) };
        return x_or_rand_below_y(result, number);
    } else return analytic_continuation(front_gauss, number);
}

Integer middle_gauss(Integer number) {
    if (number > 0) { // Narrowing Float -> Integer
        const Integer result { Integer(std::floor(random_normal(number / 2.0, number / 10.0))) };
        return x_or_rand_below_y(result, number);
    } else return analytic_continuation(middle_gauss, number);
}

Integer back_gauss(Integer number) {
    if (number > 0) {
        return number - front_gauss(number) - 1;
    } else return analytic_continuation(back_gauss, number);
}

Integer quantum_gauss(Integer number) {
    const Integer rand_num { d(3) };
    if (rand_num == 1) return front_gauss(number);
    if (rand_num == 2) return middle_gauss(number);
    return back_gauss(number);
}

Integer front_poisson(Integer number) {
    const Float PI = 3.14159265359;
    if (number > 0) {
        const Integer result { random_poisson(number / PI) };
        return x_or_rand_below_y(result, number);
    } else return analytic_continuation(front_poisson, number);
}

Integer middle_poisson(Integer number) {
    if (number > 0) {
        const Integer result { random_poisson(number / 2.0) };
        return x_or_rand_below_y(result, number);
    } else return analytic_continuation(middle_poisson, number);
}

Integer back_poisson(Integer number) {
    if (number > 0) {
        const Integer result { number - front_poisson(number) - 1 };
        return x_or_rand_below_y(result, number);
    } else return analytic_continuation(back_poisson, number);
}

Integer quantum_poisson(Integer number) {
    const Integer rand_num { d(3) };
    if (rand_num == 1) return front_poisson(number);
    if (rand_num == 2) return middle_poisson(number);
    return back_poisson(number);
}

Integer front_geometric(Integer number) {
    if (number > 0) {
        return random_discrete(number, (number-1) * (number-2), 1.0);
    } else return analytic_continuation(front_geometric, number);
}

Integer back_geometric(Integer number) {
    if (number > 0) {
        return random_discrete(number, 1.0, (number-1) * (number-2));
    } else return analytic_continuation(back_geometric, number);
}

Integer middle_geometric(Integer number) {
    if (number > 0) {
        const Integer half {number / 2};
        if (number % 2 == 1) return half + plus_or_minus_linear(half);
        if (percent_true(50)) return back_geometric(half);
        return half + front_geometric(half);
    } else return analytic_continuation(middle_geometric, number);
}

Integer quantum_geometric(Integer number) {
    const Integer rand_num { d(3) };
    if (rand_num == 1) return front_geometric(number);
    if (rand_num == 2) return middle_geometric(number);
    else return back_geometric(number);
}

Integer quantum_monty(Integer number) {
    const Integer rand_num { d(3) };
    if (rand_num == 1) return quantum_geometric(number);
    if (rand_num == 2) return quantum_gauss(number);
    return quantum_poisson(number);
}

} // end namespace Fortuna
