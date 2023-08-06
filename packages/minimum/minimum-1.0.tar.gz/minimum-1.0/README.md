# Documentation


# Installation!

Python module can be installed using Python pip. The package is hosted on [PYPI](https://pypi.org/) and [PYPI-test](https://test.pypi.org/).

```sh
pip install minimum 
```

# PYPI-test

```sh
python3 -m pip install --index-url https://test.pypi.org/simple/ minimum 
```

# PYPI

```sh
pip install minimum 
```

# Usage
 
```sh
Follow these steps after succssefully installing the package.
1. python3
2. import minimum
3. from minimum import findmin
4. findmin.find_minimum([10, 9, 8, 7, 6, 5, 1, 2, 3, 4])
# output:  INPUT: [10, 9, 8, 7, 6, 5, 1, 2, 3, 4]
            OUTPUT: 1
```

# Examples

```sh
findmin.find_minimum([10, 9, 8, 7, 6, 5, 1, 2, 3, 4])
# output:  INPUT: [10, 9, 8, 7, 6, 5, 1, 2, 3, 4]
            OUTPUT: 1
```
```sh.
findmin.find_minimum([4, 3, 2, 1.34, 6, 7, 8.5])
# output:  INPUT: [4, 3, 2, 1.34, 6, 7, 8.5]
            OUTPUT: 1.34
```
```sh
findmin.find_minimum([10, 9, 8, 5, 6, 7, 8, 0, 3, 4])
# output:  INPUT: [10, 9, 8, 5, 6, 7, 8, 0, 3, 4]
            OUTPUT: INVALID INPUT
```



