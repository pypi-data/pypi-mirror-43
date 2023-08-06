# Micropsi Programming Challenge - David Whittingham
## Brief
I should implement a Python module which can be installed using pip, including tests, with the following functionality:
* Given a vector of elements that provides a less than operator, find the minimum using as few comparisons as possible.
* The vector shall be constructed such that it is split at some point: values before the split are sorted monotonically descending, values after the split are sorted monotonically ascending.
* The less than operator be defined as the operator that works on such vectors where a < b if min(a,b) == a.

## Approach

- I decided to use the Python 3.6.0 version as this is whats currently installed on my local machine. However this is an arbitrary choice and I have no preference to using 3.6 over 3.7 or any of the other python 3 versions. Even python 2 could be used, albeit the support for 2 will end next year and python3 is the future.

- I shall adhere to PEP8 styling unless its logical to not.

- I will use [pytest](https://docs.pytest.org/en/latest/) for testing module, and in built python libraries [timeit](https://docs.python.org/3.7/library/timeit.html) and [cProfile](https://docs.python.org/3.7/library/profile.html#module-cProfile) to time and profile the my written functions and to check they are legitimate improvements over the inbuilt min() function.

- Finally I shall package the module and upload with [twine](https://pypi.org/project/twine/) to [https://pypi.org/](https://pypi.org/) making it available to be downloaded via pip install 

## Task

By the properties of the monotonicity of the ordered array elements stated above, you can make some valid assumptions about the problem. This quick sketch should give some intuition to model the problem.

![graph](graph.jpg)

As shown above, there will be only a single minimum within the array. And the task is to find it in as little operations as possible. This is thus a mathematical optimization problem.

When the size of the array is small, we could just look at each of the elements to find the minimum value. This is what the inbuilt python min() does.

I have written a function find_min_lin() that does this.
 
 This will compare at most (n-1) elements so we can say the time complexity is O(n). As the array size grows in magnitude, this approach will become very slow.

Its possible to look through the array and stop when you reach a point that the values start ascending. Comparing this to the above method, it will have the same upper bound on number of comparisons but will finish on average sooner, if the arrays minimum it not all the way to the right of the array. 

I have written a function find_min_lin_stop() that does this.

The time complexity here is of the same order O(n) so not really an improvement. 

---

This is not a continuous problem, as array only has discrete points. Therefore a method of optimization via calculus is not possible, and instead will have to implement a search algorithm, taking advantage of the properties that the array is ordered and that there are no local minima except the global minimum.
 
In simple terms, I am saying that is nothing else to get "stuck" in apart from the minimum and and thanks to the ordering of the array, we can just take the middle element, compare it with neighbouring terms and if its the smallest we output it. If not, we then move our search point in the direction of the smallest neighbour, to the mid point of the array left and repeat this process recursively. This will greatly reduce the number of comparisons and will have time complexity of order O(\log n)

This problem has two levels to it. A simplified model would be assuming the monotonic part of the array is "strictly" monotonic and that the split point is a single element. eg) \\/ not \\__/

for the simplified version, I have written find_min_binary_search()

There are two ways to get tackle the more complicated version.

A nice way to convert the problem into the simplified model is by removing repeated values. The most efficient way to do this in python is to cast it to a set, but that would potentially change the ordering, and then a ordering algorithm needs to be run to match them to the firsts list, however this would introduce many more comparsions.

Otherwise we can add a bit to the algorithm to deal with 'flat spots' in the array values. When we get to a neighbouring triplet of values that is not strictly a<b<c but something like a<b=c, then c can be ignored, and istead we take c* where c* is the next value in the array less then b. this will give a<b<c* and the binary serach approach will work with this. It shall however take more comparisons, but does not increase the order of big O time complexity unless the flat spots are bigger then the non flat spots. 

I have treid to implement this with find_min_binary_flat_spots()

In summary we have the following functions with time complexities:

|         function name        | time complexity |
|:----------------------------:|:---------------:|
|        find_min_lin()        |       O(n)      |
|      find_min_lin_stop()     |       O(n)      |
|   find_min_binary_search()   |    O(log(n))    |
| find_min_binary_flat_spots() |    O(log(n))    |


## Naming

I named the module monominmono, referencing the fact that we are looking for a minimum within a array that contains two monotonic parts. Additionally this name is not taken on pypi, therefore its readily available for me to register a package under.

## Usage

There are two ways to use the module. 

1) You just want to use the modules functionality 

2) You want to run the modules tests and edit the source code.

---

To use the module you can do a quick pip install into your python environment 

```bash
pip install monominmono

```

You can test this worked by opening a python console and running the following, with an array of your choice.

```python
import monominmono.check as mnm

array = [3, 2, 1, 2, 3]

print(mnm.find_min_binary_flat_spots(array))
```

---

To download the module including tests and timing script:

Create an virtual environment to with python version 3 and activate it, and cd to it.

Clone this repo inside your project folder using git

```bash
git clone https://github.com/01100100/micropsi

```

Now you should have a directory that looks like this:

```
micropsi
|   graph.jpg
|   LICENSE
|   profiling.py
|   README.md
|   setup.py
|   test_.py
\-- requirements.txt
+---monominmono
    |   check.py
    \-- __init__.py
```

Change into the donwloaded directory and use the package manager [pip](https://pip.pypa.io/en/stable/) and the supplied list to install the required libraries into your virtual env.

note: requirements.txt was created using pip freeze and contains dependencies for the whole of the pytests and twine module. This could be made smaller.

```bash
cd micropsi
pip install -r requirements.txt
```

## Testing

Basic unit tests have been written in test_.py for the functions written with different edge cases tested.
 
 They should be run from the command line within the activated venv.

```bash
pytest
```

If ran correctly they should output something that looks like this:

```bash
=========================== test session starts ===========================
platform win32 -- Python 3.6.0, pytest-4.3.0, py-1.8.0, pluggy-0.9.0
rootdir: C:\Users\david\Desktop\code\micropsi, inifile:
collected 5 items                                                          

test_.py .....                                                       [100%]

======================== 5 passed in 1.64 seconds =========================

```


Due to the nature of pythons default recursion depth, The test for find_min_lin_stop(big_list) fails due to recursion overflow. However this is not really a bad thing. The behaviour is expected because we have a big array and are calling the function for each element in the array, thus many calls and the overflow limit on python is 2000 by default. 

The recursion limit can be increased with sys.setrecursionlimit(n) with n being a big number. But this is not always a good thing as the recursion limit is there so we do not crash the interpreter 

I would fix this in the future by writing functions iteratively instead of recursively. 

Additionally I would refactor the the flat_spots function and look into more edge cases, and given enough time I would go as far to prove the algorithm works and terminates for all good arrays.