# Python Lodash

pylodash is collection utilities allow you working with `arrays`, `maths`, `number` and `string`

## Installation

You can install the Pylodash from [PyPI](https://pypi.org/project/pylodash/):

```
pip install pylodash
```

Pylodash is supported on Python 3.4 and above.

## How to use methods

You can call the Pylodash in your own Python code, by importing the `pylodash` package:

```
>>> from pylodash import arrays as _
>>> _.chunk(['a', 'b' , 'c', 'd'], 2)
// => [['a', 'b'], ['c', 'd']]
```

## List methods in packages

### "Array" Methods

```
_.chunk(array, [size=1])
```

**Example**

```
_.chunk(['a', 'b', 'c', 'd'], 2)
// => [['a', 'b'], ['c', 'd']]
 
_.chunk(['a', 'b', 'c', 'd'], 3)
// => [['a', 'b', 'c'], ['d']]
```
---

```
_.compact(array)
```

**Example**

```
_.compact([0, 1, False, 2, '', 3])
// => [1, 2, 3]
```

---
```
_.difference(array, [values])
```

**Example**

```
_.difference([2, 1], [2, 3])
// => [1]
```

---
```
_.drop(array, [n=1])
```

**Example**

```
_.drop([1, 2, 3])
// => [2, 3]
 
_.drop([1, 2, 3], 2)
// => [3]
 
_.drop([1, 2, 3], 5)
// => []
 
_.drop([1, 2, 3], 0)
// => [1, 2, 3]
```

---
```
_.dropRight(array, [n=1])
```

**Example**

```
_.dropRight([1, 2, 3])
// => [1, 2]
 
_.dropRight([1, 2, 3], 2)
// => [1]
 
_.dropRight([1, 2, 3], 5)
// => []
 
_.dropRight([1, 2, 3], 0)
// => [1, 2, 3]
```

---
```
_.fill(array, value, [start=0])
```

**Example**

```
array = [1, 2, 3]
 
_.fill(array, 'a')
// => ['a', 'a', 'a']
 
_.fill(Array(3), 2)
// => [2, 2, 2]
 
_.fill([4, 6, 8, 10], '*', 1, 3)
// => [4, '*', '*', 10]
```

---
```
_.indexOf(array, value, [fromIndex=0])
```

**Example**

```
_.indexOf([1, 2, 1, 2], 2)
// => 1
 
// Search from the `fromIndex`.
_.indexOf([1, 2, 1, 2], 2, 2)
// => 3
```

---
```
_.initial(array)
```

**Example**

```
_.initial([1, 2, 3])
// => [1, 2]
```

---
```
_.pull(array, [values])
```

**Example**

```
array = ['a', 'b', 'c', 'a', 'b', 'c']
 
_.pull(array, 'a', 'c')
// => ['b', 'b']
```

---
### "Math" Methods

```
_.add(augend, addend)
```

**Example**

```
_.add(6, 4)
// => 10
```

---
```
_.ceil(number, [precision=0])
```

**Example**

```
_.ceil(4.006)
// => 5
 
_.ceil(6.004, 2)
// => 6.01
 
_.ceil(6040, -2)
// => 6100
```

---
```
_.divide(dividend, divisor)
```

**Example**

```
_.divide(6, 4)
// => 1.5
```

---
```
_.floor(number, [precision=0])
```

**Example**

```
_.floor(4.006)
// => 4
 
_.floor(0.046, 2)
// => 0.04
 
_.floor(4060, -2)
// => 4000
```

---
```
_.max(array)
```

**Example**

```
_.max([4, 2, 8, 6])
// => 8
 
_.max([]);
// => undefined
```

---
```
_.mean(array)
```

**Example**

```
_.mean([4, 2, 8, 6]);
// => 5
```

---
```
_.min(array)
```

**Example**

```
_.min([4, 2, 8, 6]);
// => 2
 
_.min([]);
// => undefined
```

---
```
_.multiply(multiplier, multiplicand)
```

**Example**

```
_.multiply(6, 4)
// => 24
```

---
```
_.round(number, [precision=0])
```

**Example**

```
_.round(4.006)
// => 4
 
_.round(4.006, 2)
// => 4.01
 
_.round(4060, -2)
// => 4100
```

---
```
_.subtract(minuend, subtrahend)
```

**Example**

```
_.subtract(6, 4)
// => 2
```

---
```
_.sum(array)
```

**Example**

```
_.sum([4, 2, 8, 6])
// => 20
```

---
### "Number" Methods

```
_.clamp(number, [lower], upper)
```

**Example**

```
_.clamp(-10, -5, 5)
// => -5
 
_.clamp(10, -5, 5)
// => 5
```

---
```
_.inRange(number, [start=0], end)
```

**Example**

```
_.inRange(3, 2, 4)
// => True
 
_.inRange(4, 8)
// => True
 
_.inRange(4, 2)
// => False
 
_.inRange(2, 2)
// => False
 
_.inRange(1.2, 2)
// => True
 
_.inRange(5.2, 4)
// => False
 
_.inRange(-3, -2, -6)
// => True
```

---
```
_.random([lower=0], [upper=1], [floating])
```

**Example**

```
_.random(0, 5);
// => an integer between 0 and 5
 
_.random(5);
// => also an integer between 0 and 5
 
_.random(5, true);
// => a floating-point number between 0 and 5
 
_.random(1.2, 5.2);
// => a floating-point number between 1.2 and 5.2
```

---
### "String" Methods

```
_.camelCase([string=''])
```

**Example**

```
_.camelCase('Foo Bar')
// => 'fooBar'
 
_.camelCase('--foo-bar--')
// => 'fooBar'
 
_.camelCase('__FOO_BAR__')
// => 'fooBar'
```

---
```
_.capitalize([string=''])
```

**Example**

```
_.capitalize('FRED')
// => 'Fred'
```

---
```
_.endsWith([string=''], [target], [position=string.length])
```

**Example**

```
_.endsWith('abc', 'c')
// => True
 
_.endsWith('abc', 'b')
// => False
 
_.endsWith('abc', 'b', 2)
// => True
```

---
```
_.escape([string=''])
```

**Example**

```
_.escape('fred, barney, & pebbles')
// => 'fred, barney, &amp; pebbles'
```

---
```
_.lowerCase([string=''])
```

**Example**

```
_.lowerCase('--Foo-Bar--')
// => 'foo bar'
 
_.lowerCase('fooBar')
// => 'foo bar'
 
_.lowerCase('__FOO_BAR__')
// => 'foo bar'
```

---
```
_.lowerFirst([string=''])
```

**Example**

```
_.lowerFirst('Fred')
// => 'fred'
 
_.lowerFirst('FRED')
// => 'fRED'
```

---
```
_.pad([string=''], [length=0], [chars=' '])
```

**Example**

```
_.pad('abc', 8)
// => '  abc   '
 
_.pad('abc', 8, '_-')
// => '_-abc_-_'
 
_.pad('abc', 3)
// => 'abc'
```

---
```
_.padEnd([string=''], [length=0], [chars=' '])
```

**Example**

```
_.padEnd('abc', 6)
// => 'abc   '
 
_.padEnd('abc', 6, '_-')
// => 'abc_-_'
 
_.padEnd('abc', 3)
// => 'abc'
```

---
```
_.padStart([string=''], [length=0], [chars=' '])
```

**Example**

```
_.padStart('abc', 6)
// => '   abc'
 
_.padStart('abc', 6, '_-')
// => '_-_abc'
 
_.padStart('abc', 3)
// => 'abc'
```

---
```
_.repeat([string=''], [n=1])
```

**Example**

```
_.repeat('*', 3)
// => '***'
 
_.repeat('abc', 2)
// => 'abcabc'
 
_.repeat('abc', 0)
// => ''
```

---
```
_.replace([string=''], pattern, replacement)
```

**Example**

```
_.replace('Hi Fred', 'Fred', 'Barney')
// => 'Hi Barney'
```

---
```
_.startsWith([string=''], [target], [position=0])
```

**Example**

```
_.startsWith('abc', 'a')
// => True
 
_.startsWith('abc', 'b')
// => False
 
_.startsWith('abc', 'b', 1)
// => True
```

## Development Mode

### Building Your Package

In development mode, pylodash need install packages below to build package:

```
- setuptools >= 38.6.0
- wheel >= 0.31.0
- twine >= 1.11.0
```


Run command to build package:

```
$ python3 setup.py sdist bdist_wheel
```

### Testing Your Package

To check that your package description will render properly on PyPI, you can run twine check on the files created in dist:

```
$ twine check dist/*
```

### Uploading Your Packages

To install package to develop environment, we can use command:

```
$ python3 setup.py develop
```

To upload package to testing environment before upload to PyPI, follow step (make sure you have an account registered):

```
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

To publish your own package to PyPI, this final step is short:

```
$ twine upload dist/*
```

### *pip* install Your Package

With your package uploaded to PyPI, you can install it with pip as well:

```
$ pip install pylodash
```

To run all test cases in package, you can run command below in folder package:

```
$ nose2
```

To export test coverage to html file, run step:

```
$ nose2 --with-coverage --coverage-report html
```

## License

Copyright © 2019 All rights reserved.