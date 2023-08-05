Boonleng's Python Library
===

Just some convenient functions, color schemes, etc. for convenient coding in the future.

### Install for System-Wide Usage

Download the project:
```shell
git clone https://github.com/boonleng/blib-py.git
```

```shell
cd blib-py
```

```shell
pip install .
```

### Use It Without Instlallation

Assume you download the project into the folder `~/Developer/blib-py`, you can add the path to Python's search path

```python
import os
import sys

sys.path.insert(0, os.path.expanduser('~') + '/Developer/blib-py')

import blib
```

### Colors

![Pallete](blob/swatch-lab.png)

### Notes to Myself

My memory is no longer as good as it used to be so I'm leaving myself some notes here. Don't use them.

```shell
python setup.py sdist upload
```

```shell
python setup.py install
```

```shell
pip3 install .
```
