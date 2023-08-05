Assorted decorator functions.


Assorted decorator functions.

## Function `decorator(deco)`

Wrapper for decorator functions to support optional keyword arguments.

Examples:

    @decorator
    def dec(func, **dkw):
      ...
    @dec
    def func1(...):
      ...
    @dec(foo='bah')
    def func2(...):
      ...
