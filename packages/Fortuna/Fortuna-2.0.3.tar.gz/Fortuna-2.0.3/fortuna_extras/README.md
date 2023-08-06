# Fortuna: Random Value Generator
Fortuna replaces much of the functionality of Python's Random module, often achieving ten times better performance. Performance is not the main gaol, Fortuna's main goal is to provide a quick and easy way to build custom random generators that don't suck.

The core functionality of Fortuna is based on the RNG Storm engine. While Storm is a high quality random engine, Fortuna is not appropriate for cryptography of any kind. Fortuna is meant for games, data science, A.I. and experimental programming, not security.

Auto Install: `$ pip install Fortuna`

Installations on platforms other than MacOS may require building from source files.

### Documentation Table of Contents:
- Introduction
- Random Value Classes
    - `TruffleShuffle(Sequence)`
    - `QuantumMonty(Sequence)`
    - Weighted Choice
        - `CumulativeWeightedChoice(Table)`
        - `RelativeWeightedChoice(Table)`
    - `FlexCat(Matrix)`
- Random Value Functions
    - `random_below(upper_bound)`
    - `random_int(left_limit, right_limit)`
    - `random_range(left_limit, right_limit, step)`
    - `d(sides)`
    - `dice(rolls, sides)`
    - `plus_or_minus(number)`
    - `percent_true(truth_factor)`
- Test Suite Output
    - Distributions and performance data from the most recent build.
- Development Log
- Legal Information

## Introduction
Welcome to Fortuna! This is a labor of love, I hope you enjoy it.

##### Local Definitions:
- Value: Any python object that can be put in a list: str, int, lambda to name a few.
- Sequence: Any list like object that can be converted into a list or tuple.
    - Generators that produce Sequences also qualify.
- Table: Sequence of Pairs.
    - List of lists of two values each.
    - Tuple of tuples of two values each.
    - Generators that produce Tables also qualify.
    - The result of `zip(list_1, list_2)` also qualifies.
- Matrix: Dictionary of Sequences.
    - Generators that produce Matrices also qualify.


## Random Value Classes
### TruffleShuffle
`TruffleShuffle(list_of_values: Sequence) -> callable`
- The input Sequence can be any list like object (list, set, tuple or generator).
- The input Sequence must not be empty. Values can be any python object.
- The returned callable produces a random value from the list with a wide uniform distribution.

#### TruffleShuffle, Basic Use Case
```python
from Fortuna import TruffleShuffle


list_of_values = [1, 2, 3, 4, 5, 6]

truffle_shuffle = TruffleShuffle(list_of_values)

print(truffle_shuffle())  # prints a random value from the list_of_values.
```

**Wide Uniform Sequence**: *"Wide"* refers to the average distance between consecutive occurrences of the same item in the output sequence. The goal of this type of distribution is to keep the output sequence free of clumps while maintaining randomness and the uniform probability of each value.

This is not the same as a *flat uniform distribution*. The two distributions will be statistically similar, but the output sequences are very different. For a more general solution that offers several statistical distributions, please refer to QuantumMonty. For a more custom solution featuring discrete rarity refer to RelativeWeightedChoice and its counterpart CumulativeWeightedChoice.

**Micro-shuffle**: This is the hallmark of TruffleShuffle and how it creates a wide uniform distribution efficiently. While adjacent duplicates are forbidden, nearly consecutive occurrences of the same item are also required to be extremely rare with respect to the size of the set. This gives rise to output sequences that seem less mechanical than other random sequences. Somehow more and less random at the same time, almost human-like?

**Automatic Flattening**: TruffleShuffle and all higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error. A callable object can be any class, function, method or lambda. Mixing callable objects with un-callable objects is fully supported. Nested callable objects are fully supported. It's lambda all the way down.

To disable automatic flattening, pass the optional argument flat=False during instantiation.

Please review the code examples of each section. If higher-order functions and lambdas make your head spin, concentrate only on the first example of each section. Because `lambda(lambda) -> lambda` fixes everything for arbitrary values of 'because', 'fixes' and 'everything'.


#### Flattening
```python
from Fortuna import TruffleShuffle


flatted = TruffleShuffle([lambda: 1, lambda: 2])
print(flatted())  # will print the value 1 or 2

un_flat = TruffleShuffle([lambda: 1, lambda: 2], flat=False)
print(un_flat()())  # will print the value 1 or 2, mind the double-double parenthesis

auto_un_flat = TruffleShuffle([lambda x: x, lambda x: x + 1])
# flat=False is not required here because the lambdas can't be called without input x satisfied.
print(auto_un_flat()(1))  # will print the value 1 or 2, mind the double-double parenthesis

```


#### Mixing Static Objects with Callable Objects
```python
from Fortuna import TruffleShuffle


mixed_flat = TruffleShuffle([1, lambda: 2])
print(mixed_flat())  # will print 1 or 2

mixed_un_flat = TruffleShuffle([1, lambda: 2], flat=False) # not recommended.
print(mixed_flat())  # will print 1 or <lambda at some_address>
# This pattern is not recommended because you wont know the nature of what you get back.
# This is almost always not what you want, and always messy.
```


##### Dynamic Strings
To successfully express a dynamic string, at least one level of indirection is required.
Without an indirection the f-string would collapse into a static string too soon.

WARNING: The following example features a higher order function that takes a tuple of lambdas and returns a higher order function that returns a random lambda that returns a dynamic f-string.

```python
from Fortuna import TruffleShuffle, d


# d is a simple dice function.
brainiac = TruffleShuffle((
    lambda: f"A{d(2)}",
    lambda: f"B{d(4)}",
    lambda: f"C{d(6)}",
))

print(brainiac())  # prints a random dynamic string.
```


### QuantumMonty
`QuantumMonty(some_list: Sequence) -> callable`
- The input Sequence can be any list like object (list, set, tuple or generator).
- The input Sequence must not be empty. Values can be any python object.
- The returned callable will produce random values from the list using the selected distribution model or "monty".
- The default monty is the Quantum Monty Algorithm.

```python
from Fortuna import QuantumMonty


list_of_values = [1, 2, 3, 4, 5, 6]
quantum_monty = QuantumMonty(list_of_values)

print(quantum_monty())          # prints a random value from the list_of_values.
                                # uses the default Quantum Monty Algorithm.

print(quantum_monty.uniform())  # prints a random value from the list_of_values.
                                # uses the "uniform" monty: a flat uniform distribution.
                                # equivalent to random.choice(list_of_values) but better.
```
The QuantumMonty class represents a diverse collection of strategies for producing random values from a sequence where the output distribution is based on the method you choose. Generally speaking, each value in the sequence will have a probability that is based on its position in the sequence. For example: the "front" monty produces random values where the beginning of the sequence is geometrically more common than the back. Given enough samples the "front" monty will always converge to a 45 degree slope down for any list of unique values.

There are three primary method families: geometric, gaussian, and poisson. Each family has three base methods; 'front', 'middle', 'back', plus a 'quantum' method that incorporates all three base methods. The quantum algorithms for each family produce distributions by overlapping the probability waves of the other methods in their family. The Quantum Monty Algorithm incorporates all nine base methods.

In addition to the thirteen positional methods that are core to QuantumMonty, it also implements a uniform distribution as a simple base case.

**Automatic Flattening**: All higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error.

```python
import Fortuna


quantum_monty = Fortuna.QuantumMonty(
    ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
)

""" Each of the following methods will return a random value from the sequence.
Each method has its own unique distribution model for the same data. """

""" Flat Base Case """
quantum_monty.uniform()             # Flat Uniform Distribution

""" Geometric Positional """
quantum_monty.front()               # Geometric Descending, Triangle
quantum_monty.middle()              # Geometric Median Peak, Equilateral Triangle
quantum_monty.back()                # Geometric Ascending, Triangle
quantum_monty.quantum()             # Geometric Overlay, Saw Tooth

""" Gaussian Positional """
quantum_monty.front_gauss()         # Exponential Gamma
quantum_monty.middle_gauss()        # Scaled Gaussian
quantum_monty.back_gauss()          # Reversed Gamma
quantum_monty.quantum_gauss()       # Gaussian Overlay

""" Poisson Positional """
quantum_monty.front_poisson()       # 1/3 Mean Poisson
quantum_monty.middle_poisson()      # 1/2 Mean Poisson
quantum_monty.back_poisson()        # 2/3 Mean Poisson
quantum_monty.quantum_poisson()     # Poisson Overlay

""" Quantum Monty Algorithm """
quantum_monty.quantum_monty()       # Quantum Monty Algorithm

```

### Weighted Choice: Custom Rarity
Weighted Choice offers two strategies for selecting random values from a sequence where programmable rarity is desired. Both produce a custom distribution of values based on the weights of the values.

Flatten: Both will recursively unpack callable objects returned from the data set. Callable objects that require arguments are returned in an uncalled state. To disable this behavior pass the optional argument flat=False during instantiation. By default flat=True.

- Constructor takes a copy of a sequence of weighted value pairs... `[(weight, value), ... ]`
- Automatically optimizes the sequence for correctness and optimal call performance for large data sets.
- The sequence must not be empty, and each pair must contain a weight and a value.
- Weights must be positive integers.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some fraction of the length of the sequence.

**Automatic Flattening**: All higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error.

The following examples produce equivalent distributions with comparable performance.
The choice to use one strategy over the other is purely about which one suits you or your data best. Relative weights are easier to understand at a glance. However, many RPG Treasure Tables map rather nicely to a cumulative weighted strategy.

#### Cumulative Weight Strategy
`CumulativeWeightedChoice(weighted_table: Table) -> callable`

_Note: Logic dictates Cumulative Weights must be unique!_

```python
from Fortuna import CumulativeWeightedChoice


cum_weighted_choice = CumulativeWeightedChoice([
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),  # same as rel weight 4 because 30 - 26 = 4
])

print(cum_weighted_choice())  # prints a weighted random value
```

#### Relative Weight Strategy
`RelativeWeightedChoice(weighted_table: Table) -> callable`

```python
from Fortuna import RelativeWeightedChoice


population = ["Apple", "Banana", "Cherry", "Grape", "Lime", "Orange"]
rel_weights = [7, 4, 2, 10, 3, 4]  # Alternate zip setup.
rel_weighted_choice = RelativeWeightedChoice(zip(rel_weights, population))

print(rel_weighted_choice())  # prints a weighted random value
```

### FlexCat
`FlexCat(dict_of_lists: Matrix) -> callable`

FlexCat is a 2d QuantumMonty.

Rather than taking a sequence, FlexCat takes a Matrix: a dictionary of sequences. When the the instance is called it returns a random value from a random sequence.

The constructor takes two optional keyword arguments to specify the algorithms to be used to make random selections. The algorithm specified for selecting a key need not be the same as the one for selecting values. An optional key may be provided at call time to bypass the random key selection and select a random value from that category. Keys passed in this way must match a key in the Matrix.

By default, FlexCat will use key_bias="front" and val_bias="truffle_shuffle", this will make the top of the data structure geometrically more common than the bottom and it will truffle shuffle the sequence values. This config is known as Top Cat, it produces a descending-step distribution. Many other combinations are available.

**Automatic Flattening**: All higher-order Fortuna classes will recursively unpack callable objects returned from the data set at call time. Automatic flattening is dynamic, lazy, fault tolerant and on by default. Un-callable objects or those that require arguments will be returned in an uncalled state without error.


Algorithm Options: _See QuantumMonty & TruffleShuffle for more details._
- 'front', Geometric Descending
- 'middle', Geometric Median Peak
- 'back', Geometric Ascending
- 'quantum', Geometric Overlay
- 'front_gauss', Exponential Gamma
- 'middle_gauss', Scaled Gaussian
- 'back_gauss', Reversed Gamma
- 'quantum_gauss', Gaussian Overlay
- 'front_poisson', 1/3 Mean Poisson
- 'middle_poisson', 1/2 Mean Poisson
- 'back_poisson', 2/3 Mean Poisson
- 'quantum_poisson', Poisson Overlay
- 'quantum_monty', Quantum Monty Algorithm
- 'uniform', uniform flat distribution
- 'truffle_shuffle', TruffleShuffle, wide uniform distribution


```python
from Fortuna import FlexCat

matrix_data = {
    "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
    "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
    "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
}
flex_cat = FlexCat(matrix_data, key_bias="front", val_bias="back")

flex_cat()          # returns a random "back" value from a random "front" category
flex_cat("Cat_B")   # returns a random "back" value specifically from "Cat_B"
```

## Fortuna Functions
### Random Numbers
- `Fortuna.random_below(number: int) -> int`
    - Returns a random integer in the exclusive range:
        - [0, number) for positive values.
        - (number, 0] for negative values.
        - Always returns zero when the input is zero
    - Flat uniform distribution.


- `Fortuna.random_int(left_limit: int, right_limit: int) -> int`
    - Inclusive, fault-tolerant, efficient version of random.randint()
    - `random_int(1, 10) -> [1, 10]`
    - `random_int(10, 1) -> [1, 10]` same as above.
    - Flat uniform distribution.


- `Fortuna.random_range(left_limit: int, right_limit: int = 0, step: int = 1) -> int`
    - Inclusive, fault-tolerant, efficient version of random.randrange()
    - Returns a random integer in the range [A, B] by increments of C.
        - Where A = left_limit, B = right_limit, C = step.
    - `random_range(2, 11, 2) -> [2, 10] by 2` even numbers from 2 to 10
    - `random_range(2, 11, -2) -> [3, 11] by -2` odd numbers from 11 to 3
    - `random_range(10, 1, 0) -> [10]` a step size or range of zero always returns the first arg
    - Flat uniform distribution.


- `Fortuna.d(sides: int) -> int`
    - Represents a single die roll of a given size die.
    - Returns a random integer in the range [1, sides].
    - Flat uniform distribution.


- `Fortuna.dice(rolls: int, sides: int) -> int`
    - Returns a random integer in range [X, Y] where X = rolls and Y = rolls * sides.
    - The return value represents the sum of multiple rolls of the same size die.
    - Geometric distribution based on the number and size of the dice rolled.
    - Complexity scales primarily with the number of rolls, not the size of the dice.


- `Fortuna.plus_or_minus(number: int) -> int`
    - Returns a random integer in range [-number, number].
    - Flat uniform distribution.


### Random Truth
- `Fortuna.percent_true(truth_factor: float = 50.0) -> bool`
    - Always returns False if num is 0.0 or less
    - Always returns True if num is 100.0 or more.
    - Produces True or False based truth_factor: the probability of True as a percentage.


## Fortuna Distribution and Performance Test Suite
```
Fortuna Test Suite: RNG Storm Engine

TruffleShuffle
Output Analysis: TruffleShuffle([4, 8, 10, 18, 16, 14, 20, 12, 6, 2, 0], flat=True)()
Approximate Single Execution Time: Min: 500ns, Mid: 812ns, Max: 5093ns
Raw Samples: 14, 20, 2, 8, 16, 6, 18, 12, 4, 0
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 10
 Maximum: 20
 Mean: 9.98588
 Std Deviation: 6.327549367994694
Sample Distribution:
 0: 9.27%
 2: 8.998%
 4: 9.015%
 6: 9.077%
 8: 9.271%
 10: 8.931%
 12: 9.145%
 14: 9.056%
 16: 9.12%
 18: 9.096%
 20: 9.021%


QuantumMonty([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
Output Distribution: QuantumMonty.uniform()
Approximate Single Execution Time: Min: 187ns, Mid: 218ns, Max: 437ns
Raw Samples: 20, 16, 4, 6, 16, 20, 0, 12, 4, 4
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 10
 Maximum: 20
 Mean: 9.99796
 Std Deviation: 6.338580094498779
Sample Distribution:
 0: 9.205%
 2: 9.191%
 4: 8.916%
 6: 9.111%
 8: 9.102%
 10: 8.929%
 12: 9.077%
 14: 9.068%
 16: 9.108%
 18: 9.243%
 20: 9.05%

Output Distribution: QuantumMonty.front()
Approximate Single Execution Time: Min: 531ns, Mid: 562ns, Max: 1031ns
Raw Samples: 10, 16, 2, 2, 8, 8, 2, 2, 12, 6
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 6
 Maximum: 20
 Mean: 6.53554
 Std Deviation: 5.294706530826092
Sample Distribution:
 0: 17.019%
 2: 15.335%
 4: 13.843%
 6: 12.226%
 8: 10.682%
 10: 9.043%
 12: 7.439%
 14: 5.991%
 16: 4.423%
 18: 2.81%
 20: 1.189%

Output Distribution: QuantumMonty.back()
Approximate Single Execution Time: Min: 562ns, Mid: 562ns, Max: 1000ns
Raw Samples: 14, 14, 8, 18, 6, 20, 8, 12, 14, 8
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 14
 Maximum: 20
 Mean: 13.46722
 Std Deviation: 5.282081452935458
Sample Distribution:
 0: 1.208%
 2: 2.749%
 4: 4.441%
 6: 5.834%
 8: 7.529%
 10: 9.136%
 12: 10.591%
 14: 12.309%
 16: 13.943%
 18: 15.421%
 20: 16.839%

Output Distribution: QuantumMonty.middle()
Approximate Single Execution Time: Min: 187ns, Mid: 218ns, Max: 343ns
Raw Samples: 10, 20, 2, 16, 10, 4, 10, 4, 8, 10
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 10
 Maximum: 20
 Mean: 9.99756
 Std Deviation: 4.826599942720556
Sample Distribution:
 0: 2.779%
 2: 5.55%
 4: 8.325%
 6: 11.048%
 8: 13.893%
 10: 16.936%
 12: 13.754%
 14: 11.016%
 16: 8.457%
 18: 5.43%
 20: 2.812%

Output Distribution: QuantumMonty.quantum()
Approximate Single Execution Time: Min: 468ns, Mid: 500ns, Max: 1187ns
Raw Samples: 10, 8, 8, 10, 16, 16, 14, 12, 20, 0
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 10
 Maximum: 20
 Mean: 9.98518
 Std Deviation: 5.878156674915951
Sample Distribution:
 0: 7.051%
 2: 7.962%
 4: 8.899%
 6: 9.74%
 8: 10.786%
 10: 11.293%
 12: 10.819%
 14: 9.696%
 16: 8.881%
 18: 7.894%
 20: 6.979%

Output Distribution: QuantumMonty.front_gauss()
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 406ns
Raw Samples: 2, 2, 0, 0, 0, 0, 2, 2, 0, 0
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 0
 Maximum: 20
 Mean: 1.34446
 Std Deviation: 2.1081251742525877
Sample Distribution:
 0: 59.703%
 2: 24.092%
 4: 9.73%
 6: 3.897%
 8: 1.564%
 10: 0.594%
 12: 0.255%
 14: 0.111%
 16: 0.041%
 18: 0.011%
 20: 0.002%

Output Distribution: QuantumMonty.back_gauss()
Approximate Single Execution Time: Min: 156ns, Mid: 187ns, Max: 562ns
Raw Samples: 18, 18, 16, 20, 18, 20, 12, 20, 20, 20
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 20
 Maximum: 20
 Mean: 18.64736
 Std Deviation: 2.1272353611443227
Sample Distribution:
 0: 0.005%
 2: 0.023%
 4: 0.038%
 6: 0.099%
 8: 0.26%
 10: 0.649%
 12: 1.571%
 14: 3.941%
 16: 9.783%
 18: 23.9%
 20: 59.731%

Output Distribution: QuantumMonty.middle_gauss()
Approximate Single Execution Time: Min: 187ns, Mid: 218ns, Max: 406ns
Raw Samples: 12, 12, 10, 12, 12, 10, 10, 12, 8, 8
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 10
 Maximum: 18
 Mean: 9.9924
 Std Deviation: 2.272723892763687
Sample Distribution:
 0: 0.001%
 2: 0.077%
 4: 1.08%
 6: 7.481%
 8: 23.962%
 10: 35.078%
 12: 23.78%
 14: 7.381%
 16: 1.085%
 18: 0.075%

Output Distribution: QuantumMonty.quantum_gauss()
Approximate Single Execution Time: Min: 250ns, Mid: 250ns, Max: 625ns
Raw Samples: 10, 6, 10, 2, 10, 18, 20, 12, 10, 20
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 10
 Maximum: 20
 Mean: 9.99364
 Std Deviation: 7.373190841815496
Sample Distribution:
 0: 19.832%
 2: 7.992%
 4: 3.625%
 6: 3.861%
 8: 8.645%
 10: 12.183%
 12: 8.576%
 14: 3.88%
 16: 3.64%
 18: 8.034%
 20: 19.732%

Output Distribution: QuantumMonty.front_poisson()
Approximate Single Execution Time: Min: 218ns, Mid: 250ns, Max: 937ns
Raw Samples: 6, 20, 8, 8, 4, 0, 8, 12, 10, 4
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 6
 Maximum: 20
 Mean: 6.9626
 Std Deviation: 3.7043026953239915
Sample Distribution:
 0: 3.103%
 2: 10.637%
 4: 18.406%
 6: 21.909%
 8: 18.783%
 10: 13.123%
 12: 7.686%
 14: 3.825%
 16: 1.669%
 18: 0.626%
 20: 0.233%

Output Distribution: QuantumMonty.back_poisson()
Approximate Single Execution Time: Min: 187ns, Mid: 218ns, Max: 750ns
Raw Samples: 12, 12, 12, 12, 12, 16, 12, 18, 14, 8
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 14
 Maximum: 20
 Mean: 13.0034
 Std Deviation: 3.711027641673068
Sample Distribution:
 0: 0.235%
 2: 0.65%
 4: 1.63%
 6: 3.935%
 8: 7.828%
 10: 13.295%
 12: 18.868%
 14: 21.681%
 16: 18.264%
 18: 10.559%
 20: 3.055%

Output Distribution: QuantumMonty.middle_poisson()
Approximate Single Execution Time: Min: 218ns, Mid: 218ns, Max: 375ns
Raw Samples: 10, 8, 10, 10, 14, 8, 8, 2, 6, 6
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 10
 Maximum: 20
 Mean: 10.63286
 Std Deviation: 4.340824420310787
Sample Distribution:
 0: 0.66%
 2: 2.471%
 4: 6.429%
 6: 11.622%
 8: 15.964%
 10: 17.421%
 12: 15.999%
 14: 12.366%
 16: 8.653%
 18: 5.443%
 20: 2.972%

Output Distribution: QuantumMonty.quantum_poisson()
Approximate Single Execution Time: Min: 250ns, Mid: 250ns, Max: 593ns
Raw Samples: 14, 8, 16, 10, 16, 4, 20, 18, 8, 10
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 10
 Maximum: 20
 Mean: 10.27056
 Std Deviation: 4.659533710463311
Sample Distribution:
 0: 1.289%
 2: 4.403%
 4: 8.766%
 6: 12.427%
 8: 14.063%
 10: 14.509%
 12: 14.054%
 14: 12.781%
 16: 9.797%
 18: 5.762%
 20: 2.149%

Output Distribution: QuantumMonty.quantum_monty()
Approximate Single Execution Time: Min: 312ns, Mid: 343ns, Max: 562ns
Raw Samples: 20, 6, 4, 4, 16, 20, 16, 0, 12, 8
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 10
 Maximum: 20
 Mean: 10.05776
 Std Deviation: 6.085878257206729
Sample Distribution:
 0: 9.473%
 2: 6.876%
 4: 7.097%
 6: 8.75%
 8: 11.072%
 10: 12.758%
 12: 11.146%
 14: 8.647%
 16: 7.251%
 18: 7.223%
 20: 9.707%


Weighted Choice
Output Analysis: CumulativeWeightedChoice(<zip object at 0x10d19ec48>, flat=True)()
Approximate Single Execution Time: Min: 312ns, Mid: 312ns, Max: 531ns
Raw Samples: 18, 18, 18, 18, 18, 18, 18, 18, 18, 18
Test Samples: 100000
Sample Statistics:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.65922
 Std Deviation: 2.085203220869545
Sample Distribution:
 18: 90.068%
 24: 8.971%
 30: 0.867%
 36: 0.094%

Output Analysis: RelativeWeightedChoice(<zip object at 0x10d19ec88>, flat=True)()
Approximate Single Execution Time: Min: 312ns, Mid: 343ns, Max: 500ns
Raw Samples: 24, 18, 18, 24, 18, 18, 18, 24, 18, 18
Test Samples: 100000
Sample Statistics:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6621
 Std Deviation: 2.089982600471282
Sample Distribution:
 18: 90.021%
 24: 9.025%
 30: 0.852%
 36: 0.102%


FlexCat
Output Analysis: FlexCat({1: [1, 2, 3], 2: [10, 20, 30], 3: [100, 200, 300]}, key_bias='front', val_bias='truffle_shuffle', flat=True)()
Approximate Single Execution Time: Min: 1250ns, Mid: 1312ns, Max: 1687ns
Raw Samples: 20, 30, 100, 2, 300, 20, 30, 1, 20, 30
Test Samples: 100000
Sample Statistics:
 Minimum: 1
 Median: 20
 Maximum: 300
 Mean: 65.2192
 Std Deviation: 96.90934973252403
Sample Distribution:
 1: 12.624%
 2: 12.576%
 3: 12.588%
 10: 11.125%
 20: 11.087%
 30: 11.093%
 100: 9.645%
 200: 9.625%
 300: 9.637%


Random Numbers
Output Distribution: random_below(10)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 343ns
Raw Samples: 0, 8, 6, 6, 8, 0, 6, 9, 5, 5
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.51202
 Std Deviation: 2.872674371066171
Sample Distribution:
 0: 9.872%
 1: 10.0%
 2: 10.004%
 3: 10.052%
 4: 9.888%
 5: 10.033%
 6: 9.994%
 7: 9.992%
 8: 10.072%
 9: 10.093%

Output Distribution: random_int(-5, 5)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 218ns
Raw Samples: 5, 3, -3, -3, -1, 1, -2, 2, -5, 3
Test Samples: 100000
Sample Statistics:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.01549
 Std Deviation: 3.1569335948349027
Sample Distribution:
 -5: 9.179%
 -4: 9.073%
 -3: 9.081%
 -2: 9.145%
 -1: 9.115%
 0: 9.117%
 1: 9.152%
 2: 9.102%
 3: 9.18%
 4: 8.89%
 5: 8.966%

Output Distribution: random_range(1, 20, 2)
Approximate Single Execution Time: Min: 62ns, Mid: 93ns, Max: 156ns
Raw Samples: 3, 7, 13, 17, 15, 9, 5, 1, 13, 19
Test Samples: 100000
Sample Statistics:
 Minimum: 1
 Median: 9
 Maximum: 19
 Mean: 9.95438
 Std Deviation: 5.747118330893413
Sample Distribution:
 1: 10.09%
 3: 10.158%
 5: 10.062%
 7: 10.098%
 9: 9.944%
 11: 9.962%
 13: 9.968%
 15: 9.961%
 17: 9.791%
 19: 9.966%

Output Distribution: d(10)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 125ns
Raw Samples: 3, 9, 7, 8, 5, 2, 6, 2, 6, 5
Test Samples: 100000
Sample Statistics:
 Minimum: 1
 Median: 6
 Maximum: 10
 Mean: 5.51038
 Std Deviation: 2.869898015391172
Sample Distribution:
 1: 9.906%
 2: 9.999%
 3: 9.904%
 4: 9.929%
 5: 10.119%
 6: 10.046%
 7: 10.048%
 8: 10.048%
 9: 9.895%
 10: 10.106%

Output Distribution: dice(2, 6)
Approximate Single Execution Time: Min: 93ns, Mid: 93ns, Max: 187ns
Raw Samples: 11, 8, 4, 7, 10, 10, 10, 6, 6, 11
Test Samples: 100000
Sample Statistics:
 Minimum: 2
 Median: 7
 Maximum: 12
 Mean: 7.00356
 Std Deviation: 2.414660562533857
Sample Distribution:
 2: 2.787%
 3: 5.514%
 4: 8.292%
 5: 11.112%
 6: 13.93%
 7: 16.591%
 8: 14.017%
 9: 11.076%
 10: 8.288%
 11: 5.621%
 12: 2.772%

Output Distribution: percent_true(33.33)
Approximate Single Execution Time: Min: 31ns, Mid: 62ns, Max: 250ns
Raw Samples: False, False, False, False, False, False, False, False, False, True
Test Samples: 100000
Sample Statistics:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.33288
 Std Deviation: 0.4712463541835239
Sample Distribution:
 False: 66.712%
 True: 33.288%

Output Distribution: plus_or_minus(5)
Approximate Single Execution Time: Min: 62ns, Mid: 62ns, Max: 156ns
Raw Samples: 0, -3, 3, 4, 0, -1, -5, 5, 1, -5
Test Samples: 100000
Sample Statistics:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: -0.00838
 Std Deviation: 3.1571742829775062
Sample Distribution:
 -5: 9.03%
 -4: 9.022%
 -3: 9.353%
 -2: 9.066%
 -1: 9.123%
 0: 9.038%
 1: 9.198%
 2: 9.131%
 3: 8.939%
 4: 9.063%
 5: 9.037%


Base Cases
Output Distribution: Random.randrange(10)
Approximate Single Execution Time: Min: 843ns, Mid: 875ns, Max: 1218ns
Raw Samples: 5, 4, 7, 1, 5, 3, 7, 9, 7, 4
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 4
 Maximum: 9
 Mean: 4.50022
 Std Deviation: 2.870104933033506
Sample Distribution:
 0: 9.974%
 1: 9.915%
 2: 10.179%
 3: 9.839%
 4: 10.106%
 5: 10.1%
 6: 9.863%
 7: 10.006%
 8: 10.074%
 9: 9.944%

Output Distribution: Random.randint(-5, 5)
Approximate Single Execution Time: Min: 1125ns, Mid: 1187ns, Max: 1875ns
Raw Samples: -5, 5, 5, -4, 5, -4, 1, 2, -2, 2
Test Samples: 100000
Sample Statistics:
 Minimum: -5
 Median: 0
 Maximum: 5
 Mean: 0.02245
 Std Deviation: 3.156134599372481
Sample Distribution:
 -5: 8.818%
 -4: 9.133%
 -3: 9.052%
 -2: 9.054%
 -1: 9.076%
 0: 9.141%
 1: 9.099%
 2: 9.093%
 3: 9.366%
 4: 9.016%
 5: 9.152%

Output Distribution: Random.randrange(1, 21, 2)
Approximate Single Execution Time: Min: 1312ns, Mid: 1375ns, Max: 2531ns
Raw Samples: 7, 11, 9, 5, 17, 13, 13, 13, 15, 15
Test Samples: 100000
Sample Statistics:
 Minimum: 1
 Median: 9
 Maximum: 19
 Mean: 10.0089
 Std Deviation: 5.7387603298710115
Sample Distribution:
 1: 9.93%
 3: 10.04%
 5: 9.85%
 7: 9.99%
 9: 10.219%
 11: 10.04%
 13: 9.887%
 15: 9.993%
 17: 10.073%
 19: 9.978%

Output Distribution: Random.choice([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
Approximate Single Execution Time: Min: 750ns, Mid: 781ns, Max: 1062ns
Raw Samples: 8, 20, 8, 12, 18, 6, 6, 0, 10, 14
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 10
 Maximum: 20
 Mean: 9.97906
 Std Deviation: 6.302228074037544
Sample Distribution:
 0: 8.948%
 2: 9.114%
 4: 9.155%
 6: 9.252%
 8: 9.178%
 10: 9.13%
 12: 9.077%
 14: 9.076%
 16: 9.132%
 18: 9.019%
 20: 8.919%

Output Distribution: Random.choices([36, 30, 24, 18], weights=[1, 9, 90, 900])
Approximate Single Execution Time: Min: 2125ns, Mid: 2171ns, Max: 2781ns
Raw Samples: [18], [24], [18], [18], [24], [18], [24], [18], [18], [18]
Test Samples: 100000
Sample Statistics:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.6753
 Std Deviation: 2.1208429667820523
Sample Distribution:
 18: 89.892%
 24: 9.067%
 30: 0.935%
 36: 0.106%

Output Distribution: Random.choices([36, 30, 24, 18], cum_weights=[1, 10, 100, 1000])
Approximate Single Execution Time: Min: 1687ns, Mid: 1687ns, Max: 2250ns
Raw Samples: [18], [18], [18], [18], [18], [18], [18], [18], [18], [18]
Test Samples: 100000
Sample Statistics:
 Minimum: 18
 Median: 18
 Maximum: 36
 Mean: 18.66534
 Std Deviation: 2.0968659119902084
Sample Distribution:
 18: 89.977%
 24: 9.068%
 30: 0.844%
 36: 0.111%


Experimental: RNG Vortex Engine
Output Distribution: vortex_random_below(10)
Approximate Single Execution Time: Min: 93ns, Mid: 125ns, Max: 406ns
Raw Samples: 7, 5, 9, 7, 2, 9, 6, 3, 3, 3
Test Samples: 100000
Sample Statistics:
 Minimum: 0
 Median: 5
 Maximum: 9
 Mean: 4.5014
 Std Deviation: 2.872807088929868
Sample Distribution:
 0: 10.123%
 1: 9.865%
 2: 10.02%
 3: 9.955%
 4: 9.835%
 5: 10.115%
 6: 10.028%
 7: 10.07%
 8: 10.104%
 9: 9.885%

```


## Fortuna Development Log
##### Fortuna 2.0.3
- Bug fix.

##### Fortuna 2.0.2
- Clarified some documentation.

##### Fortuna 2.0.1
- Fixed some typos.

##### Fortuna 2.0.0b1-10
- Total rebuild. New RNG Storm Engine.

##### Fortuna 1.26.7.1
- README updated.

##### Fortuna 1.26.7
- Small bug fix.

##### Fortuna 1.26.6
- Updated README to reflect recent changes to the test script.

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
- Moved README and LICENSE files into fortuna_extras folder.

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
