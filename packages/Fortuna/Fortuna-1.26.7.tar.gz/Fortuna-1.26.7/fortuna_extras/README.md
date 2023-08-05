# Fortuna: Fast & Flexible Random Value Generators
Fortuna replaces much of the functionality of Python's Random module, often achieving 10x better performance. However, the most interesting bits of Fortuna are found in the high-level abstractions like FlexCat, QuantumMonty and TruffleShuffle.

The core functionality of Fortuna is based on the Mersenne Twister Algorithm by Makoto Matsumoto (松本 眞) and Takuji Nishimura (西村 拓士). Fortuna is not appropriate for cryptography of any kind. Fortuna is for games, data science, AI and experimental programming, not security.

The Fortuna generator was designed to use hardware seeding exclusively. This allows the generator to be completely encapsulated.

Installation: `$ pip install Fortuna` or you can download and build from source. Building Fortuna requires the latest version of Python3, Cython, python3 dev tools, and a modern C++17 compiler. Fortuna is designed, built and tested for MacOS X, and also happens to work with many flavors of Linux. Fortuna is not officially supported on Windows at this time.

Fortuna is built for the default CPython implementation standard, other implementations may or may not support c-extensions like Fortuna. A pure Python version of Fortuna is included in the extras folder. The Fortuna c-extension is roughly an order of magnitude faster than the pure Python version, but they offer the same API and functionality.


## Documentation Table of Contents
```
I.   Fortuna Core Functions
        a. Random Numbers
        b. Random Truth
        c. Random Sequence Values
        d. Random Table Values

II.  Fortuna Abstraction Classes
        a. Sequence Wrappers
            1. TruffleShuffle
            2. QuantumMonty
        b. Weighted Table Wrappers
            1. Cumulative Weighted Choice
            2. Relative Weighted Choice
        c. Dictionary Wrapper
            1. FlexCat

III. Test Suite, output distributions and performance data.

IV.  Development Log

V.   Legal Information

```

---

## Fortuna Random Functions
### Random Numbers
`Fortuna.random_range(lo: int, hi: int) -> int`. Returns a random integer in range [lo..hi] inclusive. Up to 15x faster than `random.randint()`. Flat uniform distribution.

`Fortuna.random_below(num: int) -> int`. Returns a random integer in the exclusive range [0..num) for positive values of num. Flat uniform distribution.

`Fortuna.d(sides: int) -> int`. Represents a single die roll of a given size die. Returns a random integer in the range [1..sides]. Flat uniform distribution.

`Fortuna.dice(rolls: int, sides: int) -> int`. Returns a random integer in range [X..Y] where X = rolls and Y = rolls * sides. The return value represents the sum of multiple rolls of the same size die. Geometric distribution based on the number and size of the dice rolled. Complexity scales primarily with the number of rolls, not the size of the dice.

`Fortuna.plus_or_minus(num: int) -> int`. Negative and positive input values of num will produce equivalent distributions. Returns a random integer in range [-num..num]. Flat uniform distribution.

`Fortuna.plus_or_minus_linear(num: int) -> int`. Returns a random integer in range [-num..num]. Zero peak geometric distribution, up triangle.

`Fortuna.plus_or_minus_curve(num: int) -> int`. Returns a random integer in the bounded range [-num..num]. Zero peak gaussian distribution, bounded stretched bell curve: mean = 0, variance = num / pi.

`Fortuna.plus_or_minus_linear_down(num: int) -> int`. Returns a random integer in range [-num..num]. Edge peak geometric distribution, down triangle. Inverted plus_or_minus_linear.

`Fortuna.plus_or_minus_curve_down(num: int) -> int`. Returns a random integer in the range [-num..num]. Edge peak gaussian distribution, upside down bell curve. Inverted plus_or_minus_curve.

`Fortuna.zero_flat(num: int) -> int`. Returns a random integer in range [0..num]. Flat uniform distribution.

`Fortuna.zero_cool(num: int) -> int`. Returns a random integer in range [0..num]. Zero peak, geometric distribution, lefthand triangle.

`Fortuna.zero_extreme(num: int) -> int`. Returns a random integer in range [0..num]. Zero peak, gaussian distribution, half bell curve.

`Fortuna.max_cool(num: int) -> int`. Returns a random integer in range [0..num]. Max peak (num), geometric distribution, righthand triangle.

`Fortuna.max_extreme(num: int) -> int`. Returns a random integer in range [0..num]. Max peak (num), gaussian distribution, half bell curve.

`Fortuna.mostly_middle(num: int) -> int`. Returns a random integer in range [0..num]. Middle peak (num / 2), geometric distribution, up triangle. Ranges that span an even number of values will have two dominant values in the middle rather than one, this will guarantee that the probability distribution is always symmetrical.

`Fortuna.mostly_center(num: int) -> int`. Returns a random integer in range [0..num]. Middle peak (num / 2), gaussian distribution, bell curve: mean = num / 2, variance = num / pi.

`Fortuna.mostly_not_middle(num: int) -> int`. Returns a random integer in range [0..num]. Edge peaks, geometric distribution, down triangle. Ranges that span an even number of values will have two dominant values in the middle rather than one, this will guarantee that the probability distribution is always symmetrical.

`Fortuna.mostly_not_center(num: int) -> int`. Returns a random integer in range [0..num]. Edge peaks, gaussian distribution, upside down bell curve.

`Fortuna.random_float() -> float`. Returns a random float in range [0.0..1.0) exclusive. Same as random.random().


### Random Truth
`Fortuna.percent_true(num: int) -> bool`. Always returns False if num is 0 or less, always returns True if num is 100 or more. Any value of num in range [1..99] will produce True or False based on the value of num - the probability of True as a percentage.

`Fortuna.percent_true_float(num: float) -> bool`. Always returns False if num is 0.0 or less, always returns True if num is 100.0 or more. It will produce True or False based on the value of num - the probability of True as a percentage. Same as percent_true but with floating point accuracy.


### Random Sequence Values
`Fortuna.random_value(arr) -> value`. Returns a random value from a sequence (list or tuple), uniform distribution, non-destructive. Up to 10x faster than random.choice().

`Fortuna.pop_random_value(arr: list) -> value`. Returns and removes a random value from a sequence list, uniform distribution, destructive. Not included in the test suite due to it's destructive nature. This is the only destructive function in the module, use with care. It will raise an error if the list is empty.

`Fortuna.shuffle(arr: list) -> None`. Alternate Fisher-Yates Shuffle Algorithm. More than an order of magnitude faster than random.shuffle().


### Random Table Values
`Fortuna.cumulative_weighted_choice(table) -> value`. Core function for the WeightedChoice base class. Produces a custom distribution of values based on cumulative weights. Requires input format: `[(weight, value), ... ]` sorted in ascending order by weight. Weights must be unique positive integers. See WeightedChoice class for a more comprehensive solution that verifies and optimizes the table. Up to 15x faster than random.choices()


## Fortuna Random Classes
### Sequence Wrappers
#### Truffle Shuffle
Returns a random value from the wrapped sequence.

Produces a uniform distribution with a wide spread. Longer sequences will naturally push duplicates even farther apart. This behavior gives rise to output sequences that seem less mechanical than other random sequences.

Flatten: TruffleShuffle will recursively unpack callable objects returned from the data set. Callable objects that require arguments are returned in an uncalled state. To disable this behavior pass the optional argument flat=False during instantiation. By default flat=True. A callable object is any function, method or lambda.

- Constructor takes a copy of a sequence (generator, list or tuple) of arbitrary values.
- Values can be any Python object that can be passed around.
- Features continuous smart micro-shuffling: The Truffle Shuffle.
- Performance scales by some small fraction of the length of the input sequence.

```python
from Fortuna import TruffleShuffle


truffle_shuffle = TruffleShuffle(["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"])
truffle_shuffle()  # returns a random value, cycled uniform distribution.
```


#### The Quantum Monty
QuantumMonty is a set of strategies for producing random values from a sequence where the probability of each value is based on the method or "monty" you choose. For example: the mostly_front monty produces random values where the beginning of the sequence is geometrically more common than the back. This always produces a 45 degree slope down no matter how many values are in the data.

The Quantum Monty Algorithm is special, it produces values by overlapping the probability waves of six of the other methods. The distribution it produces is a gentle curve up towards the middle with a distinct bump in the center of the sequence.

Flatten: QuantumMonty will recursively unpack callable objects returned from the data set. Callable objects that require arguments are not called. To disable this behavior pass the optional argument flat=False during instantiation. By default flat=True.

- Constructor takes a copy of a sequence (generator, list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some tiny fraction of the length of the sequence. Method scaling may vary slightly.

```python
from Fortuna import QuantumMonty


quantum_monty = QuantumMonty(["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"])

# Each of the following methods will return a random value from the sequence.
quantum_monty.mostly_front()        # Mostly from the front of the list (geometric descending)
quantum_monty.mostly_middle()       # Mostly from the middle of the list (geometric pyramid)
quantum_monty.mostly_back()         # Mostly from the back of the list (geometric ascending)
quantum_monty.mostly_first()        # Mostly from the very front of the list (stretched gaussian descending)
quantum_monty.mostly_center()       # Mostly from the very center of the list (stretched gaussian bell curve)
quantum_monty.mostly_last()         # Mostly from the very back of the list (stretched gaussian ascending)
quantum_monty.quantum_monty()       # Quantum Monty Algorithm. Overlapping probability waves.
quantum_monty.mostly_flat()         # Uniform flat distribution (see Fortuna.random_value if this is the only behavior you need.)
quantum_monty.mostly_cycle()        # Cycled uniform flat distribution (see TruffleShuffle)
quantum_monty.mostly_not_middle()   # Mostly from the edges of the list (geometric upside down pyramid)
quantum_monty.mostly_not_center()   # Mostly from the outside edges of the list (inverted gaussian bell curve)
quantum_monty.quantum_not_monty()   # Inverted Quantum Monty Algorithm.
```


### Table Wrappers
#### Weighted Choice: Custom Rarity
Weighted Choice offers two strategies for selecting random values from a sequence where programmable rarity is desired. Both produce a custom distribution of values based on the weights of the values. Both are up to 10x faster than random.choices()

Flatten: Both will recursively unpack callable objects returned from the data set. Callable objects that require arguments are returned in an uncalled state. To disable this behavior pass the optional argument flat=False during instantiation. By default flat=True.

- Constructor takes a copy of a sequence of weighted value pairs... `[(weight, value), ... ]`
- Automatically optimizes the sequence for correctness and optimal call performance for large data sets.
- The sequence must not be empty, and each pair must contain a weight and a value.
- Weights must be positive integers.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some fraction of the length of the sequence.

The following examples produce equivalent distributions with comparable performance.
The choice to use one strategy over the other is purely about which one suits you or your data best. Relative weights are easier to understand at a glance. However, many RPG Treasure Tables map rather nicely to a cumulative weighted strategy.


##### Cumulative Weight Strategy
_Note: Logic dictates Cumulative Weights must be unique!_

```python
from Fortuna import CumulativeWeightedChoice


cumulative_weighted_choice = CumulativeWeightedChoice([
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),
])

cumulative_weighted_choice()  # returns a weighted random value
```


##### Relative Weight Strategy
Relative weights work just like cumulative weights, except each weight is comparable to the others.


```python
from Fortuna import RelativeWeightedChoice


relative_weighted_choice = RelativeWeightedChoice([
    (7, "Apple"),
    (4, "Banana"),
    (2, "Cherry"),
    (10, "Grape"),
    (3, "Lime"),
    (4, "Orange"),
])

relative_weighted_choice()  # returns a weighted random value
```


### Dictionary Wrappers
#### FlexCat
FlexCat wraps a dictionary of sequences. When the primary method is called it returns a random value from one of the sequences. It takes two optional keyword arguments to specify the algorithms used to make random selections.

By default, FlexCat will use y_bias="front" and x_bias="cycle", this will make the top of the data structure geometrically more common than the bottom and cycle the sequences. This config is known as Top Cat, it produces a descending-step cycled distribution for the data. Many other combinations are possible (12 algorithms, 2 dimensions = 144 possible configurations).

FlexCat generally works best if all sequences in a set are sufficiently large and close to the same size, this is not enforced. Values in a shorter sequence will naturally be more common, since probability balancing between categories is not considered. For example: in a flat/flat set where it might be expected that all values have equal probability (and they would, given sequences with equal length). However, values in a sequence half the size of the others in the set would have exactly double the probability of the other items. This effect scales with the size delta and affects all nine methods. Cross category balancing might be considered for a future release.

Flatten: FlexCat will recursively unpack callable objects returned from the data set. Callable objects that require arguments are returned in an uncalled state. To disable this behavior pass the optional argument flat=False during instantiation. By default flat=True.


Algorithm Options: _See QuantumMonty & TruffleShuffle for more details._
- front, geometric descending
- middle, geometric pyramid
- back, geometric ascending
- first, stretched gaussian descending
- center, stretched gaussian bell
- last, stretched gaussian ascending
- monty, The Quantum Monty
- flat, uniform flat
- cycle, TruffleShuffle uniform flat
- not_middle, favors the top and bottom of the list, geometric upside down pyramid
- not_center, favors the top and bottom of the list, stretched gaussian upside down bell
- not_monty, inverted Quantum Monty

```python
from Fortuna import FlexCat


flex_cat = FlexCat({
    "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
    "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
    "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
}, y_bias="front", x_bias="cycle")

flex_cat()          # returns a random value from a random category
flex_cat("Cat_A")   # returns a random value from "Cat_A"
flex_cat("Cat_B")   #                             "Cat_B"
flex_cat("Cat_C")   #                             "Cat_C"
```


## Fortuna Test Suite
#### Testbed:
- **Software:** _macOS 10.14.3, Python 3.7.2, Fortuna Extension._
- **Hardware:** _Intel 2.7GHz i7 Skylake, 16GB RAM, 1TB SSD._

```
Fortuna Extension v1.26.7

Base Cases: Python3 Random Module
-------------------------------------------------------------------------
random.randint(-6, 6):
Time: Min: 1375ns, Mode: 1406ns, Mean: 1426ns, Max: 1687ns
-6: 7.35%
-5: 7.49%
-4: 7.86%
-3: 7.79%
-2: 7.66%
-1: 8.11%
0: 7.45%
1: 7.42%
2: 7.94%
3: 7.32%
4: 7.93%
5: 8.01%
6: 7.67%

random.randrange(-6, 6):
Time: Min: 1187ns, Mode: 1218ns, Mean: 1226ns, Max: 1437ns
-6: 8.5%
-5: 8.02%
-4: 8.5%
-3: 8.62%
-2: 8.49%
-1: 8.49%
0: 7.99%
1: 8.52%
2: 8.33%
3: 7.93%
4: 8.23%
5: 8.38%

random.choice(population):
Time: Min: 718ns, Mode: 718ns, Mean: 763ns, Max: 1187ns
Apple: 14.02%
Banana: 14.88%
Cherry: 14.3%
Grape: 14.13%
Lime: 14.03%
Orange: 14.28%
Pineapple: 14.36%

random.choices(population, cum_weights=cum_weights):
Time: Min: 1718ns, Mode: 1750ns, Mean: 1779ns, Max: 2312ns
Apple: 20.3%
Banana: 12.12%
Cherry: 5.7%
Grape: 28.21%
Lime: 8.77%
Orange: 11.35%
Pineapple: 13.55%

random.choices(population, weights=rel_weights):
Time: Min: 2218ns, Mode: 2250ns, Mean: 2255ns, Max: 2468ns
Apple: 19.57%
Banana: 11.61%
Cherry: 5.77%
Grape: 27.98%
Lime: 8.84%
Orange: 11.27%
Pineapple: 14.96%

random.shuffle(population):
Time: Min: 4781ns, Mode: N/A, Mean: 4926ns, Max: 5250ns

random.random():
Time: Min: 31ns, Mode: 31ns, Mean: 43ns, Max: 62ns


Test Cases: Fortuna Functions
-------------------------------------------------------------------------
random_range(-6, 6):
Time: Min: 62ns, Mode: 62ns, Mean: 70ns, Max: 125ns
-6: 8.06%
-5: 7.62%
-4: 7.47%
-3: 7.59%
-2: 7.31%
-1: 7.47%
0: 7.6%
1: 7.63%
2: 8.04%
3: 7.71%
4: 7.4%
5: 8.08%
6: 8.02%

random_below(6):
Time: Min: 62ns, Mode: 62ns, Mean: 63ns, Max: 93ns
0: 16.29%
1: 16.84%
2: 16.72%
3: 17.02%
4: 16.52%
5: 16.61%

d(6):
Time: Min: 62ns, Mode: 62ns, Mean: 63ns, Max: 93ns
1: 16.5%
2: 17.0%
3: 17.15%
4: 16.0%
5: 16.55%
6: 16.8%

dice(3, 6):
Time: Min: 93ns, Mode: 125ns, Mean: 124ns, Max: 156ns
3: 0.38%
4: 1.07%
5: 2.73%
6: 4.72%
7: 6.48%
8: 10.08%
9: 11.21%
10: 12.59%
11: 12.83%
12: 11.76%
13: 9.61%
14: 7.09%
15: 4.85%
16: 2.48%
17: 1.68%
18: 0.44%

plus_or_minus(6):
Time: Min: 62ns, Mode: 62ns, Mean: 65ns, Max: 93ns
-6: 7.59%
-5: 7.47%
-4: 8.31%
-3: 7.88%
-2: 7.42%
-1: 7.62%
0: 7.73%
1: 7.82%
2: 7.44%
3: 7.15%
4: 7.84%
5: 7.7%
6: 8.03%

plus_or_minus_linear(6):
Time: Min: 62ns, Mode: 93ns, Mean: 87ns, Max: 125ns
-6: 2.24%
-5: 4.32%
-4: 6.22%
-3: 8.35%
-2: 9.68%
-1: 12.43%
0: 13.91%
1: 12.27%
2: 9.9%
3: 8.17%
4: 6.04%
5: 4.42%
6: 2.05%

plus_or_minus_curve(6):
Time: Min: 125ns, Mode: 125ns, Mean: 134ns, Max: 156ns
-6: 0.17%
-5: 0.92%
-4: 2.5%
-3: 5.69%
-2: 11.76%
-1: 18.27%
0: 20.64%
1: 18.31%
2: 11.81%
3: 6.29%
4: 2.65%
5: 0.8%
6: 0.19%

plus_or_minus_linear_down(6):
Time: Min: 156ns, Mode: 218ns, Mean: 204ns, Max: 218ns
-6: 12.35%
-5: 10.71%
-4: 9.68%
-3: 7.5%
-2: 5.28%
-1: 3.94%
0: 1.72%
1: 3.5%
2: 5.24%
3: 7.44%
4: 8.71%
5: 11.12%
6: 12.81%

plus_or_minus_curve_down(6):
Time: Min: 218ns, Mode: 281ns, Mean: 270ns, Max: 312ns
-6: 17.53%
-5: 15.04%
-4: 9.84%
-3: 5.08%
-2: 2.23%
-1: 0.63%
0: 0.16%
1: 0.6%
2: 1.93%
3: 5.48%
4: 9.93%
5: 14.4%
6: 17.15%

zero_flat(6):
Time: Min: 31ns, Mode: 62ns, Mean: 61ns, Max: 62ns
0: 14.52%
1: 14.3%
2: 13.76%
3: 14.31%
4: 14.02%
5: 14.8%
6: 14.29%

zero_cool(6):
Time: Min: 93ns, Mode: 125ns, Mean: 130ns, Max: 156ns
0: 25.03%
1: 21.58%
2: 17.67%
3: 13.98%
4: 10.57%
5: 7.3%
6: 3.87%

zero_extreme(6):
Time: Min: 156ns, Mode: 218ns, Mean: 200ns, Max: 250ns
0: 34.18%
1: 30.06%
2: 19.91%
3: 10.48%
4: 4.09%
5: 1.04%
6: 0.24%

max_cool(6):
Time: Min: 93ns, Mode: 125ns, Mean: 127ns, Max: 156ns
0: 3.33%
1: 7.28%
2: 10.52%
3: 14.11%
4: 18.78%
5: 21.35%
6: 24.63%

max_extreme(6):
Time: Min: 187ns, Mode: 187ns, Mean: 200ns, Max: 250ns
0: 0.24%
1: 1.24%
2: 4.06%
3: 10.2%
4: 19.23%
5: 30.73%
6: 34.3%

mostly_middle(6):
Time: Min: 62ns, Mode: 93ns, Mean: 95ns, Max: 500ns
0: 6.01%
1: 12.44%
2: 18.57%
3: 25.23%
4: 18.85%
5: 12.63%
6: 6.27%

mostly_center(6):
Time: Min: 125ns, Mode: 125ns, Mean: 135ns, Max: 156ns
0: 0.36%
1: 5.22%
2: 24.16%
3: 40.12%
4: 24.29%
5: 5.33%
6: 0.52%

mostly_not_middle(6):
Time: Min: 156ns, Mode: 187ns, Mean: 180ns, Max: 187ns
0: 20.98%
1: 16.3%
2: 10.06%
3: 4.93%
4: 10.6%
5: 16.07%
6: 21.06%

mostly_not_center(6):
Time: Min: 218ns, Mode: 250ns, Mean: 242ns, Max: 281ns
0: 28.58%
1: 16.83%
2: 3.86%
3: 0.38%
4: 3.67%
5: 18.22%
6: 28.46%

random_value(population):
Time: Min: 31ns, Mode: 62ns, Mean: 61ns, Max: 93ns
Apple: 14.4%
Banana: 14.25%
Cherry: 13.96%
Grape: 13.98%
Lime: 14.48%
Orange: 14.44%
Pineapple: 14.49%

percent_true(30):
Time: Min: 31ns, Mode: 62ns, Mean: 61ns, Max: 93ns
False: 69.49%
True: 30.51%

percent_true_float(33.33):
Time: Min: 62ns, Mode: 62ns, Mean: 78ns, Max: 125ns
False: 66.59%
True: 33.41%

random_float():
Time: Min: 31ns, Mode: 31ns, Mean: 45ns, Max: 62ns

shuffle(population):
Time: Min: 187ns, Mode: 218ns, Mean: 217ns, Max: 250ns


Test Cases: Fortuna Classes
-------------------------------------------------------------------------
cum_weighted_choice():
Time: Min: 343ns, Mode: 343ns, Mean: 366ns, Max: 687ns
Apple: 19.69%
Banana: 11.77%
Cherry: 5.82%
Grape: 28.63%
Lime: 8.48%
Orange: 11.09%
Pineapple: 14.52%

rel_weighted_choice():
Time: Min: 343ns, Mode: 375ns, Mean: 365ns, Max: 531ns
Apple: 19.69%
Banana: 11.9%
Cherry: 5.55%
Grape: 27.96%
Lime: 8.71%
Orange: 11.85%
Pineapple: 14.34%

truffle_shuffle():
Time: Min: 343ns, Mode: 375ns, Mean: 376ns, Max: 468ns
Apple: 14.22%
Banana: 14.63%
Cherry: 13.78%
Grape: 14.36%
Lime: 14.52%
Orange: 14.41%
Pineapple: 14.08%

quantum_monty.mostly_flat():
Time: Min: 156ns, Mode: 187ns, Mean: 182ns, Max: 343ns
Apple: 14.39%
Banana: 13.99%
Cherry: 14.24%
Grape: 13.81%
Lime: 14.3%
Orange: 14.99%
Pineapple: 14.28%

quantum_monty.mostly_middle():
Time: Min: 187ns, Mode: 187ns, Mean: 195ns, Max: 312ns
Apple: 6.27%
Banana: 12.43%
Cherry: 18.47%
Grape: 25.24%
Lime: 18.55%
Orange: 12.31%
Pineapple: 6.73%

quantum_monty.mostly_center():
Time: Min: 250ns, Mode: 250ns, Mean: 255ns, Max: 406ns
Apple: 0.46%
Banana: 5.52%
Cherry: 23.62%
Grape: 40.02%
Lime: 24.42%
Orange: 5.48%
Pineapple: 0.48%

quantum_monty.mostly_front():
Time: Min: 250ns, Mode: 250ns, Mean: 263ns, Max: 312ns
Apple: 24.89%
Banana: 21.95%
Cherry: 17.11%
Grape: 13.49%
Lime: 11.05%
Orange: 7.95%
Pineapple: 3.56%

quantum_monty.mostly_back():
Time: Min: 218ns, Mode: 250ns, Mean: 244ns, Max: 281ns
Apple: 3.49%
Banana: 7.12%
Cherry: 10.66%
Grape: 14.27%
Lime: 17.41%
Orange: 22.07%
Pineapple: 24.98%

quantum_monty.mostly_first():
Time: Min: 281ns, Mode: 312ns, Mean: 328ns, Max: 375ns
Apple: 34.08%
Banana: 29.67%
Cherry: 20.03%
Grape: 10.43%
Lime: 4.15%
Orange: 1.33%
Pineapple: 0.31%

quantum_monty.mostly_last():
Time: Min: 281ns, Mode: 312ns, Mean: 381ns, Max: 1187ns
Apple: 0.32%
Banana: 1.31%
Cherry: 4.26%
Grape: 10.11%
Lime: 19.9%
Orange: 28.92%
Pineapple: 35.18%

quantum_monty.mostly_cycle():
Time: Min: 437ns, Mode: 468ns, Mean: 473ns, Max: 687ns
Apple: 14.24%
Banana: 14.08%
Cherry: 14.53%
Grape: 14.45%
Lime: 14.41%
Orange: 14.14%
Pineapple: 14.15%

quantum_monty.quantum_monty():
Time: Min: 593ns, Mode: 625ns, Mean: 634ns, Max: 843ns
Apple: 12.02%
Banana: 12.62%
Cherry: 16.72%
Grape: 19.29%
Lime: 15.85%
Orange: 12.32%
Pineapple: 11.18%

quantum_monty.mostly_not_middle():
Time: Min: 281ns, Mode: 312ns, Mean: 301ns, Max: 375ns
Apple: 21.21%
Banana: 15.68%
Cherry: 10.94%
Grape: 4.91%
Lime: 9.8%
Orange: 15.59%
Pineapple: 21.87%

quantum_monty.mostly_not_center():
Time: Min: 343ns, Mode: 375ns, Mean: 370ns, Max: 437ns
Apple: 29.18%
Banana: 16.7%
Cherry: 3.76%
Grape: 0.31%
Lime: 3.66%
Orange: 17.66%
Pineapple: 28.73%

quantum_monty.quantum_not_monty():
Time: Min: 625ns, Mode: 656ns, Mean: 677ns, Max: 906ns
Apple: 18.4%
Banana: 15.4%
Cherry: 11.68%
Grape: 9.16%
Lime: 10.69%
Orange: 15.56%
Pineapple: 19.11%

flex_cat():
Time: Min: 750ns, Mode: 781ns, Mean: 962ns, Max: 1281ns
A1: 16.78%
A2: 16.77%
A3: 16.64%
B1: 11.24%
B2: 11.2%
B3: 11.11%
C1: 5.29%
C2: 5.36%
C3: 5.61%

flex_cat('Cat_A'):
Time: Min: 468ns, Mode: 468ns, Mean: 484ns, Max: 531ns
A1: 33.82%
A2: 33.1%
A3: 33.08%

flex_cat('Cat_B'):
Time: Min: 468ns, Mode: 500ns, Mean: 493ns, Max: 656ns
B1: 32.94%
B2: 33.8%
B3: 33.26%

flex_cat('Cat_C'):
Time: Min: 468ns, Mode: 500ns, Mean: 537ns, Max: 1343ns
C1: 33.44%
C2: 33.72%
C3: 32.84%

```


## Fortuna Development Log
##### Fortuna 1.26.7
- Small bug fix.

##### Fortuna 1.26.6
- Updated README.md to reflect recent changes to the test script.

##### Fortuna 1.26.5
- Fixed small bug in test script.

##### Fortuna 1.26.4
- Updated documentation for clarity.
- Fixed a minor typo in the test script.

##### Fortuna 1.26.3
- Clean build.

##### Fortuna 1.26.2
- Fixed some minor typos.

##### Fortuna 1.26.1
- Release.

##### Fortuna 1.26.0 beta 2
- Moved README.md and LICENSE files into fortuna_extras folder.

##### Fortuna 1.26.0 beta 1
- Dynamic version scheme implemented.
- The Fortuna Extension now requires the fortuna_extras package, previously it was optional.

##### Fortuna 1.25.4
- Fixed some minor typos in the test script.

##### Fortuna 1.25.3
- Since version 1.24 Fortuna requires Python 3.7 or higher. This patch corrects an issue where the setup script incorrectly reported requiring Python 3.6 or higher.

##### Fortuna 1.25.2
- Updated test suite.
- Major performance update for TruffleShuffle.
- Minor performance update for QuantumMonty & FlexCat: cycle monty.

##### Fortuna 1.25.1
- Important bug fix for TruffleShuffle, QuantumMonty and FlexCat.

##### Fortuna 1.25
- Full 64bit support.
- The Distribution & Performance Tests have been redesigned.
- Bloat Control: Two experimental features have been removed.
    - RandomWalk
    - CatWalk
- Bloat Control: Several utility functions have been removed from the top level API. These function remain in the Fortuna namespace for now, but may change in the future without warning.
    - stretch_bell, internal only.
    - min_max, not used anymore.
    - analytic_continuation, internal only.
    - flatten, internal only.

##### Fortuna 1.24.3
- Low level refactoring, non-breaking patch.

##### Fortuna 1.24.2
- Setup config updated to improve installation.

##### Fortuna 1.24.1
- Low level patch to avoid potential ADL issue. All low level function calls are now qualified.

##### Fortuna 1.24
- Documentation updated for even more clarity.
- Bloat Control: Two naïve utility functions that are no longer used in the module have been removed.
    - n_samples -> use a list comprehension instead. `[f(x) for _ in range(n)]`
    - bind -> use a lambda instead. `lambda: f(x)`

##### Fortuna 1.23.7
- Documentation updated for clarity.
- Minor bug fixes.
- TruffleShuffle has been redesigned slightly, it now uses a random rotate instead of swap.
- Custom `__repr__` methods have been added to each class.

##### Fortuna 1.23.6
- New method for QuantumMonty: quantum_not_monty - produces the upside down quantum_monty.
- New bias option for FlexCat: not_monty.

##### Fortuna 1.23.5.1
- Fixed some small typos.

##### Fortuna 1.23.5
- Documentation updated for clarity.
- All sequence wrappers can now accept generators as input.
- Six new functions added:
    - random_float() -> float in range [0.0..1.0) exclusive, uniform flat distribution.
    - percent_true_float(num: float) -> bool, Like percent_true but with floating point precision.
    - plus_or_minus_linear_down(num: int) -> int in range [-num..num], upside down pyramid.
    - plus_or_minus_curve_down(num: int) -> int in range [-num..num], upside down bell curve.
    - mostly_not_middle(num: int) -> int in range [0..num], upside down pyramid.
    - mostly_not_center(num: int) -> int in range [0..num], upside down bell curve.
- Two new methods for QuantumMonty:
    - mostly_not_middle
    - mostly_not_center
- Two new bias options for FlexCat, either can be used to define x and/or y axis bias:
    - not_middle
    - not_center

##### Fortuna 1.23.4.2
- Fixed some minor typos in the README.md file.

##### Fortuna 1.23.4.1
- Fixed some minor typos in the test suite.

##### Fortuna 1.23.4
- Fortuna is now Production/Stable!
- Fortuna and Fortuna Pure now use the same test suite.

##### Fortuna 0.23.4, first release candidate.
- RandomCycle, BlockCycle and TruffleShuffle have been refactored and combined into one class: TruffleShuffle.
- QuantumMonty and FlexCat will now use the new TruffleShuffle for cycling.
- Minor refactoring across the module.

##### Fortuna 0.23.3, internal
- Function shuffle(arr: list) added.

##### Fortuna 0.23.2, internal
- Simplified the plus_or_minus_curve(num: int) function, output will now always be bounded to the range [-num..num].
- Function stretched_bell(num: int) added, this matches the previous behavior of an unbounded plus_or_minus_curve.

##### Fortuna 0.23.1, internal
- Small bug fixes and general clean up.

##### Fortuna 0.23.0
- The number of test cycles in the test suite has been reduced to 10,000 (down from 100,000). The performance of the pure python implementation and the c-extension are now directly comparable.
- Minor tweaks made to the examples in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.22.2, experimental features
- BlockCycle class added.
- RandomWalk class added.
- CatWalk class added.

##### Fortuna 0.22.1
- Fortuna classes no longer return lists of values, this behavior has been extracted to a free function called n_samples.

##### Fortuna 0.22.0, experimental features
- Function bind added.
- Function n_samples added.

##### Fortuna 0.21.3
- Flatten will no longer raise an error if passed a callable item that it can't call. It correctly returns such items in an uncalled state without error.
- Simplified `.../fortuna_extras/fortuna_examples.py` - removed unnecessary class structure.

##### Fortuna 0.21.2
- Fix some minor bugs.

##### Fortuna 0.21.1
- Fixed a bug in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.21.0
- Function flatten added.
- Flatten: The Fortuna classes will recursively unpack callable objects in the data set.

##### Fortuna 0.20.10
- Documentation updated.

##### Fortuna 0.20.9
- Minor bug fixes.

##### Fortuna 0.20.8, internal
- Testing cycle for potential new features.

##### Fortuna 0.20.7
- Documentation updated for clarity.

##### Fortuna 0.20.6
- Tests updated based on recent changes.

##### Fortuna 0.20.5, internal
- Documentation updated based on recent changes.

##### Fortuna 0.20.4, internal
- WeightedChoice (both types) can optionally return a list of samples rather than just one value, control the length of the list via the n_samples argument.

##### Fortuna 0.20.3, internal
- RandomCycle can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.2, internal
- QuantumMonty can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.1, internal
- FlexCat can optionally return a list of samples rather than just one value,
control the length of the list via the n_samples argument.

##### Fortuna 0.20.0, internal
- FlexCat now accepts a standard dict as input. The ordered(ness) of dict is now part of the standard in Python 3.7.1. Previously FlexCat required an OrderedDict, now it accepts either and treats them the same.

##### Fortuna 0.19.7
- Fixed bug in `.../fortuna_extras/fortuna_examples.py`.

##### Fortuna 0.19.6
- Updated documentation formatting.
- Small performance tweak for QuantumMonty and FlexCat.

##### Fortuna 0.19.5
- Minor documentation update.

##### Fortuna 0.19.4
- Minor update to all classes for better debugging.

##### Fortuna 0.19.3
- Updated plus_or_minus_curve to allow unbounded output.

##### Fortuna 0.19.2
- Internal development cycle.
- Minor update to FlexCat for better debugging.

##### Fortuna 0.19.1
- Internal development cycle.

##### Fortuna 0.19.0
- Updated documentation for clarity.
- MultiCat has been removed, it is replaced by FlexCat.
- Mostly has been removed, it is replaced by QuantumMonty.

##### Fortuna 0.18.7
- Fixed some more README typos.

##### Fortuna 0.18.6
- Fixed some README typos.

##### Fortuna 0.18.5
- Updated documentation.
- Fixed another minor test bug.

##### Fortuna 0.18.4
- Updated documentation to reflect recent changes.
- Fixed some small test bugs.
- Reduced default number of test cycles to 10,000 - down from 100,000.

##### Fortuna 0.18.3
- Fixed some minor README typos.

##### Fortuna 0.18.2
- Fixed a bug with Fortuna Pure.

##### Fortuna 0.18.1
- Fixed some minor typos.
- Added tests for `.../fortuna_extras/fortuna_pure.py`

##### Fortuna 0.18.0
- Introduced new test format, now includes average call time in nanoseconds.
- Reduced default number of test cycles to 100,000 - down from 1,000,000.
- Added pure Python implementation of Fortuna: `.../fortuna_extras/fortuna_pure.py`
- Promoted several low level functions to top level.
    - `zero_flat(num: int) -> int`
    - `zero_cool(num: int) -> int`
    - `zero_extreme(num: int) -> int`
    - `max_cool(num: int) -> int`
    - `max_extreme(num: int) -> int`
    - `analytic_continuation(func: staticmethod, num: int) -> int`
    - `min_max(num: int, lo: int, hi: int) -> int`

##### Fortuna 0.17.3
- Internal development cycle.

##### Fortuna 0.17.2
- User Requested: dice() and d() functions now support negative numbers as input.

##### Fortuna 0.17.1
- Fixed some minor typos.

##### Fortuna 0.17.0
- Added QuantumMonty to replace Mostly, same default behavior with more options.
- Mostly is depreciated and may be removed in a future release.
- Added FlexCat to replace MultiCat, same default behavior with more options.
- MultiCat is depreciated and may be removed in a future release.
- Expanded the Treasure Table example in `.../fortuna_extras/fortuna_examples.py`

##### Fortuna 0.16.2
- Minor refactoring for WeightedChoice.

##### Fortuna 0.16.1
- Redesigned fortuna_examples.py to feature a dynamic random magic item generator.
- Raised cumulative_weighted_choice function to top level.
- Added test for cumulative_weighted_choice as free function.
- Updated MultiCat documentation for clarity.

##### Fortuna 0.16.0
- Pushed distribution_timer to the .pyx layer.
- Changed default number of iterations of tests to 1 million, up form 1 hundred thousand.
- Reordered tests to better match documentation.
- Added Base Case Fortuna.fast_rand_below.
- Added Base Case Fortuna.fast_d.
- Added Base Case Fortuna.fast_dice.

##### Fortuna 0.15.10
- Internal Development Cycle

##### Fortuna 0.15.9
- Added Base Cases for random.choices()
- Added Base Case for randint_dice()

##### Fortuna 0.15.8
- Clarified MultiCat Test

##### Fortuna 0.15.7
- Fixed minor typos.

##### Fortuna 0.15.6
- Fixed minor typos.
- Simplified MultiCat example.

##### Fortuna 0.15.5
- Added MultiCat test.
- Fixed some minor typos in docs.

##### Fortuna 0.15.4
- Performance optimization for both WeightedChoice() variants.
- Cython update provides small performance enhancement across the board.
- Compilation now leverages Python3 all the way down.
- MultiCat pushed to the .pyx layer for better performance.

##### Fortuna 0.15.3
- Reworked the MultiCat example to include several randomizing strategies working in concert.
- Added Multi Dice 10d10 performance tests.
- Updated sudo code in documentation to be more pythonic.

##### Fortuna 0.15.2
- Fixed: Linux installation failure.
- Added: complete source files to the distribution (.cpp .hpp .pyx).

##### Fortuna 0.15.1
- Updated & simplified distribution_timer in `fortuna_tests.py`
- Readme updated, fixed some typos.
- Known issue preventing successful installation on some linux platforms.

##### Fortuna 0.15.0
- Performance tweaks.
- Readme updated, added some details.

##### Fortuna 0.14.1
- Readme updated, fixed some typos.

##### Fortuna 0.14.0
- Fixed a bug where the analytic continuation algorithm caused a rare issue during compilation on some platforms.

##### Fortuna 0.13.3
- Fixed Test Bug: percent sign was missing in output distributions.
- Readme updated: added update history, fixed some typos.

##### Fortuna 0.13.2
- Readme updated for even more clarity.

##### Fortuna 0.13.1
- Readme updated for clarity.

##### Fortuna 0.13.0
- Minor Bug Fixes.
- Readme updated for aesthetics.
- Added Tests: `.../fortuna_extras/fortuna_tests.py`

##### Fortuna 0.12.0
- Internal test for future update.

##### Fortuna 0.11.0
- Initial Release: Public Beta

##### Fortuna 0.10.0
- Module name changed from Dice to Fortuna

##### Dice 0.1.x - 0.9.x
- Experimental Phase


## Legal Information
Fortuna © 2019 Broken aka Robert W Sharp, all rights reserved.

Fortuna is licensed under a Creative Commons Attribution-NonCommercial 3.0 Unported License.

See online version of this license here: <http://creativecommons.org/licenses/by-nc/3.0/>
