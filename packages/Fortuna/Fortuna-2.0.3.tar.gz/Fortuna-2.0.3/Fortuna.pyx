#!python3
#distutils: language = c++
import time
import math
import statistics
import random


__all__ = (
    "TruffleShuffle", "QuantumMonty", "CumulativeWeightedChoice", "RelativeWeightedChoice", "FlexCat", "LazyCat",
    "random_below", "random_int", "random_range", "d", "dice", "percent_true", "plus_or_minus", "plus_or_minus_linear",
    "ability_dice", "shuffle", "random_value", "vortex_random_below", "distribution_timer"
)

cdef extern from "Fortuna.hpp":
    int       _percent_true         "Fortuna::percent_true"(double)
    long long _random_range         "Fortuna::random_range"(long long, long long, int)
    long long _vortex_random_below "Fortuna::vortex_random_below"(long long)
    long long _random_below         "Fortuna::random_below"(long long)
    long long _random_int           "Fortuna::random_int"(long long, long long)
    long long _d                    "Fortuna::d"(long long)
    long long _dice                 "Fortuna::dice"(long long, long long)
    long long _ability_dice         "Fortuna::ability_dice"(long long)
    long long _plus_or_minus        "Fortuna::plus_or_minus"(long long)
    long long _plus_or_minus_linear "Fortuna::plus_or_minus_linear"(long long)
    long long _front_gauss          "Fortuna::front_gauss"(long long)
    long long _middle_gauss         "Fortuna::middle_gauss"(long long)
    long long _back_gauss           "Fortuna::back_gauss"(long long)
    long long _quantum_gauss        "Fortuna::quantum_gauss"(long long)
    long long _front_poisson        "Fortuna::front_poisson"(long long)
    long long _middle_poisson       "Fortuna::middle_poisson"(long long)
    long long _back_poisson         "Fortuna::back_poisson"(long long)
    long long _quantum_poisson      "Fortuna::quantum_poisson"(long long)
    long long _front_geometric      "Fortuna::front_geometric"(long long)
    long long _middle_geometric     "Fortuna::middle_geometric"(long long)
    long long _back_geometric       "Fortuna::back_geometric"(long long)
    long long _quantum_geometric    "Fortuna::quantum_geometric"(long long)
    long long _quantum_monty        "Fortuna::quantum_monty"(long long)


def random_range(left_limit, right_limit=0, step=1):
    return _random_range(left_limit, right_limit, step)


def random_below(upper_bound):
    return _random_below(upper_bound)


def vortex_random_below(upper_bound):
    return _vortex_random_below(upper_bound)


def random_int(left_limit, right_limit):
    return _random_int(left_limit, right_limit)


def d(sides=20):
    return _d(sides)


def dice(rolls=1, sides=20):
    return _dice(rolls, sides)


def ability_dice(rolls=4):
    return _ability_dice(rolls)


def plus_or_minus(number):
    return _plus_or_minus(number)


def plus_or_minus_linear(number):
    return _plus_or_minus_linear(number)


def percent_true(truth_factor=50.0) -> bool:
    return _percent_true(truth_factor) == 1


def front_gauss(upper_bound):
    return _front_gauss(upper_bound)


def middle_gauss(upper_bound):
    return _middle_gauss(upper_bound)


def back_gauss(upper_bound):
    return _back_gauss(upper_bound)


def quantum_gauss(upper_bound):
    return _quantum_gauss(upper_bound)


def front_poisson(upper_bound):
    return _front_poisson(upper_bound)


def middle_poisson(upper_bound):
    return _middle_poisson(upper_bound)


def back_poisson(upper_bound):
    return _back_poisson(upper_bound)


def quantum_poisson(upper_bound):
    return _quantum_poisson(upper_bound)


def front_geometric(upper_bound):
    return _front_geometric(upper_bound)


def middle_geometric(upper_bound):
    return _middle_geometric(upper_bound)


def back_geometric(upper_bound):
    return _back_geometric(upper_bound)


def quantum_geometric(upper_bound):
    return _quantum_geometric(upper_bound)


def quantum_monty(upper_bound):
    return _quantum_monty(upper_bound)


def random_value(arr):
    size = len(arr)
    return arr[_random_below(size)]


def cumulative_weighted_choice(table):
    max_weight = table[-1][0]
    rand = _random_below(max_weight)
    for weight, value in table:
        if weight > rand:
            return value


def flatten(itm, flat=True):
    if flat is False or not callable(itm):
        return itm
    else:
        try:
            return flatten(itm())
        except TypeError:
            return itm


def shuffle(arr):
    size = len(arr)
    for i in range(1, size):
        j = _random_int(0, i)
        arr[i], arr[j] = arr[j], arr[i]


class TruffleShuffle:
    __slots__ = ("data", "flat", "size")

    def __init__(self, arr, flat=True):
        size = len(arr)
        assert size is not 0, "Input Error, Empty Container"
        self.size = size - 1
        self.data = list(arr)
        self.flat = flat
        shuffle(self.data)

    def __call__(self):
        return flatten(self.random_rotate(), self.flat)

    def __str__(self):
        return f"TruffleShuffle({self.data}, flat={self.flat})"

    def random_rotate(self):
        result = self.data.pop()
        self.data.insert(_front_poisson(self.size), result)
        return result


class QuantumMonty:
    __slots__ = ("flat", "size", "data", "truffle_shuffle")

    def __init__(self, arr, flat=True):
        self.flat = flat
        self.size = len(arr)
        self.data = tuple(arr)
        self.truffle_shuffle = TruffleShuffle(arr, flat)

    def __call__(self):
        return self.quantum_monty()

    def __repr__(self):
        return f"QuantumMonty({self.arr}, flat={self.flat})"

    def dispatch(self, monty):
        return {
            "uniform": self.uniform,
            "truffle_shuffle": self.truffle_shuffle,
            "front": self.front,
            "middle": self.middle,
            "back": self.back,
            "quantum": self.quantum,
            "front_gauss": self.front_gauss,
            "middle_gauss": self.middle_gauss,
            "back_gauss": self.back_gauss,
            "quantum_gauss": self.quantum_gauss,
            "front_poisson": self.front_poisson,
            "middle_poisson": self.middle_poisson,
            "back_poisson": self.back_poisson,
            "quantum_poisson": self.quantum_poisson,
            "quantum_monty": self.quantum_monty,
        }[monty]

    def uniform(self):
        return flatten(self.data[_random_below(self.size)], self.flat)

    def front(self):
        return flatten(self.data[_front_geometric(self.size)], self.flat)

    def middle(self):
        return flatten(self.data[_middle_geometric(self.size)], self.flat)

    def back(self):
        return flatten(self.data[_back_geometric(self.size)], self.flat)

    def quantum(self):
        return flatten(self.data[_quantum_geometric(self.size)], self.flat)

    def front_gauss(self):
        return flatten(self.data[_front_gauss(self.size)], self.flat)

    def middle_gauss(self):
        return flatten(self.data[_middle_gauss(self.size)], self.flat)

    def back_gauss(self):
        return flatten(self.data[_back_gauss(self.size)], self.flat)

    def quantum_gauss(self):
        return flatten(self.data[_quantum_gauss(self.size)], self.flat)

    def front_poisson(self):
        return flatten(self.data[_front_poisson(self.size)], self.flat)

    def middle_poisson(self):
        return flatten(self.data[_middle_poisson(self.size)], self.flat)

    def back_poisson(self):
        return flatten(self.data[_back_poisson(self.size)], self.flat)

    def quantum_poisson(self):
        return flatten(self.data[_quantum_poisson(self.size)], self.flat)

    def quantum_monty(self):
        return flatten(self.data[_quantum_monty(self.size)], self.flat)


class FlexCat:
    __slots__ = ("data", "flat", "key_bias", "val_bias", "random_cat", "random_selection")

    def __init__(self, data, key_bias="front", val_bias="truffle_shuffle", flat=True):
        self.data = data
        self.flat = flat
        self.key_bias = key_bias
        self.val_bias = val_bias
        self.random_cat = QuantumMonty(tuple(data.keys())).dispatch(key_bias)
        self.random_selection = {
            key: QuantumMonty(sequence, flat).dispatch(val_bias) for key, sequence in data.items()
        }

    def __call__(self, cat_key=None):
        return self.random_selection[cat_key if cat_key else self.random_cat()]()

    def __repr__(self):
        return f"FlexCat({self.data}, key_bias='{self.key_bias}', val_bias='{self.val_bias}', flat={self.flat})"


class RelativeWeightedChoice:
    __slots__ = ("weighted_table", "flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        self.weighted_table = weighted_table
        self.flat = flat
        optimized_data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)

    def __call__(self):
        result = self.weighted_choice()
        return flatten(result, self.flat)

    def __repr__(self):
        return f"RelativeWeightedChoice({self.weighted_table}, flat={self.flat})"

    def weighted_choice(self):
        rand = _random_below(self.max_weight)
        for weight, value in self.data:
            if weight > rand:
                return value


class CumulativeWeightedChoice:
    __slots__ = ("weighted_table", "flat", "max_weight", "data")

    def __init__(self, weighted_table, flat=True):
        self.weighted_table = weighted_table
        self.flat = flat
        data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0])
        prev_weight = 0
        for w_pair in data:
            w_pair[0], prev_weight = w_pair[0] - prev_weight, w_pair[0]
        optimized_data = sorted(data, key=lambda x: x[0], reverse=True)
        cum_weight = 0
        for w_pair in optimized_data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        self.max_weight = optimized_data[-1][0]
        self.data = tuple(tuple(itm) for itm in optimized_data)

    def __call__(self):
        result = self.weighted_choice()
        return flatten(result, self.flat)

    def __repr__(self):
        return f"CumulativeWeightedChoice({self.weighted_table}, flat={self.flat})"

    def weighted_choice(self):
        rand = _random_below(self.max_weight)
        for weight, value in self.data:
            if weight > rand:
                return value


class LazyCat:
    __slots__ = ("data", "func", "flat")

    def __init__(self, data, func: staticmethod = None, flat=True):
        self.data = list(data)
        self.func = func or _random_below
        self.flat = flat

    def __getitem__(self, idx: int):
        return flatten(self.data[idx], self.flat)

    def __setitem__(self, idx: int, value):
        self.data[idx] = value

    def __len__(self):
        return len(self.data)

    def __call__(self, func: staticmethod = None):
        f = func or self.func
        return self[f(len(self))]

    def __str__(self):
        return f"LazyCat({self.data}, func={self.func}, flat={self.flat})"

    def append(self, value):
        self.data.append(value)

    def pop(self, idx: int = -1):
        return self.data.pop(idx)

    def insert(self, idx: int, value):
        self.data.insert(idx, value)


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


def any_distribution(func: staticmethod, *args, num_cycles=100000, **kwargs):
    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    unique_results = list(set(results))
    if all([not callable(x) and hasattr(x, "__lt__") for x in unique_results]):
        unique_results.sort()
    result_obj = {
        key: f"{results.count(key) / (num_cycles / 100)}%" for key in unique_results
    }
    for key, val in result_obj.items():
        print(f"{key}: {val}")


def any_distribution_timer(func: staticmethod, *args, label="", **kwargs):
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
    any_distribution(func, *args, **kwargs)
    print("")


def distribution(func: staticmethod, *args, num_cycles, post_processor: staticmethod = None, **kwargs):
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


def distribution_timer(func: staticmethod, *args, num_cycles=100000, label="", post_processor=None, **kwargs):
    def samples(func, *args, **kwargs):
        return f', '.join(str(func(*args, **kwargs)) for _ in range(10))

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
