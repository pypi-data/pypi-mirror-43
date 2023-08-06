# CHANGELOG
The story begins at early february 2019

### 0.1 - initial release
* supported arguments: positional, variadic and default 
* interfaces: `reproduction_string` function and `reproducible` decorator

#### 0.1.1 - minor improvements
* `reproduction_string` can take arbitrary instance and try to evaluate its *nice repr* at runtime
* project hosted on gitlab

### 0.2 - slight interface change
* `reproduction_string` function renamed to `reproduction`
* adding tox env for python 3.7 
#### 0.2.1 - kitchen work
* package's readme back in `rst` format (less environmental mess)
* adding tox env pypy
#### 0.2.2
* remove wrapping long string with brackets if it's not
called on top-level in passed object tree
* code coverage raised up to 94%

### 0.3.0 - adding serializer and changing interface 
* interface changed `reproducible` becomes reserved for a base object
implementing `renew` methods, it's renamed to `make_renew_reprs` 
* adding inheritance extension
* adding serialization helper
* testenv: adding coverage measurement
