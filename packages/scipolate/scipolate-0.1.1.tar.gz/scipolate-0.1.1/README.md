SciPolate
=========

Scipolate offers a small helper class that can be used to perform 
2D interpolation tasks using scipy. It is meant to be used as a common 
interface to run and validate the task automated in the same way.

Installation
============

Install Scipolate using pip:

```bash
pip install scipolate
```

Note
====

Scipolate was originally a part of a interpolation web-app used in one of my 
lectures. That means it was used in an API. Hence, the parameters are set in 
one single JSON-like dictionary, which is un-pythonic and I am planning to 
create another interface class that takes arguments in a used, pythonic way.

For the same reason, the class does provide an output *Report* including the 
result as a base64 encoded image. Nevertheless, the class can be used outside 
of a web-application context. Mind that performance was not important during 
development. In case you need a fast algorithm, use scipy directly, or 
something like the [interpolation](https://pypi.org/project/interpolation/) 
library.

Usage
=====

There are two main interfaces that can be used:

* The *Interpolator* class, which is the core class performing the 
interpolation, as well as applying validation and storing meta data

* The *interpolate* method, which returns an instance of Interpolator, that 
can be used right away.

The main difference is, that the class itself requires the parameters to be 
passed as a single JSON-like dictionary (because the package was designed to 
be used in a web API). The function takes different arguments and builds that
 object for convenience. An instance of *Interpolator* has the `__call__` 
 method implemented, which returns the result as a numpy array. This way, it 
 can be used like most other scipy classes.
 
 Example
 -------
 This will be demonstrated by a small example, very similar to the one of the
[scipy.griddata documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html).
 
We will use different methods to interpolate this function:
 ```python
 import numpy as np
 def func(x, y):
     return np.sin(0.02*np.pi*y) * np.cos(0.02*np.pi*x)
```

Take random coordinate samples in 0 <= {x,y} <= 100:
```python
np.random.seed(42)
x = np.random.randint(100, size=300)
np.random.seed(1337)
y = np.random.randint(100, size=300)
z = func(x, y)
```

The `interpolate` method takes an algorithm name, the `x` and `y` coordinate 
arrays and the `z` target values array. All need to be 1D arrays. 
The grid will be automatically created, we just need to give the grid size in
the coordinate system unit. The validation should be disabled in this case, 
as we just want to display the result and do not care about the 
`Interpolator` object. Any other keyword argument will be passed down to the
`Interpolator` class.
 
 ```python
 from scipolate import interpolate
 
 near = interpolate('nearest', x, y, z, gridsize=1, validation=None)
 cub = interpolate('cubic', x ,y, z, gridsize=1, validation=None)
 svm = interpolate('svm', x, y, z, gridsize=1, validation=None)
 rbf = interpolate('rbf', x, y, z, gridsize=1, validation=None,  func='thin_plate', smooth=0.1)
 idw = interpolate('idw', x, y, z, gridsize=1, validation=None, radius=50, exp=3)
```

Which results in the image shown below:

![](compare.png)

In case, you enable validation (up to now there is only the `'jacknife'` or 
*leave-one-out* cross validation available), you can open the `report` 
attribute of each `Interpolator` instance, which contains a lot of infos, like:

```python
for alg in (near, idw, svm, rbf, cub):
    print('%s:' % alg.interp.get('func'))
    print('------------')
    print('Took:', '%.3f sec' % alg.report['took'])
    print('RMSE:', '%.3f' % alg.report['validation']['rmse'])
    print('Res.:', '%.3f' % alg.report['validation']['residual'])
    print()
```
```text
nearest:
------------
Took: 0.005 sec
RMSE: 0.102
Res.: 0.074

idw:
------------
Took: 8.147 sec
RMSE: 0.173
Res.: 0.123

svm:
------------
Took: 0.034 sec
RMSE: 0.108
Res.: 0.092

rbf:
------------
Took: 0.111 sec
RMSE: 0.013
Res.: 0.004

cubic:
------------
Took: 0.010 sec
RMSE: 0.011
Res.: 0.004
```