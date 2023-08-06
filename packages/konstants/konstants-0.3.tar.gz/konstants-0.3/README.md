# Constant List
>Python package for common math and physics constants.

[![Build Status](https://travis-ci.org/thisisjustinm/constant-list.svg?branch=master)](https://travis-ci.org/thisisjustinm/constant-list)

This is a basic and simple python package which contains all commonly used mathematical and physical constants like pi,e etc. The package is not complete and will be updated whenever I get free time. Contribs are welcome.

## Installation

Windows, OS X and Linux:  ```pip install konstants ```

## Usage

The module is very easy to use. Just search for the constant you wish to use from [here](https://raw.githubusercontent.com/thisisjustinm/constant-list/master/list.txt) and import it. To import, follow the code snippet below:

```
from konstants.math import basic as b
from konstants.math import eDerivatives as ed
from konstants.math import piDerivatives as pd
from konstants.math import named as n
from konstants.phys import fundamental as f
from konstants.phys import astrophysical as a
from konstants.misc import biblical as bi
from konstants.misc import interesting as i

print(b.pi)
print(b.e)
print(ed.eie)
print(pd.pip)
print(n.her)
print(n.ape)
print(f.amc)
print(a.par)
print(bi.ht)
print(i.ans)
```

## Release History

* 0.0.3
	* Added Miscellanous important numbers
* 0.0.2
	* Added more constants
* 0.0.1
	* Created package

##  Meta

Justin Mathew - [@thisismjustin](https://twitter.com/thisismjustin) - thisisjustinm@outlook.com

