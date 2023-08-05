`mkdict`: a multi-key dictionary
================================

Usage
-----

The ``mkdict.MultiKeyDict`` provides a multiple keyed dictionary.

When adding an element you can specify a tuple of keys:

``` python
d = MultiKeyDict()

d[1,2,3] = 123
d[1,2,4] = 124
d[2,3,4] = 234
d[3,3,4] = 334
```
All keys should have the same length otherwise a `KeyError` will be raised. 

To retrieve values you can use `None` as a wildcard character.
``` python
d[1,2,3]  -> 123
d[1,None,None] -> {(2,3): 123, (2,4): 124}
d[1,None,3] -> {(2,): 123}
```
When a wildcard is used the dictionary returns a new view on the dictionary with that key eliminated.  
When no wildcard is used the result is a single item.

Modifications of the resulting dictionary will update the parent dictionary.
For example,
``` python
d[2,None,None][4,5] = 245
```
will add the value 245 with key (2, 4, 5) in the original dictionary.

License
-------

MIT License

Copyright (c) 2019 Anton Dries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



