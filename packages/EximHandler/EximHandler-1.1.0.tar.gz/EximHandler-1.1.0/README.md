# eximhandler

A simple logging handler class which sends an email using exim.

Available on PyPI for install:

    pip install eximhandler

## Usage

```python
import logging
from eximhandler import EximHandler

exim_handler = EximHandler('me@mydomain.com', 'Hello world')
exim_handler.setLevel(logging.ERROR)

logger = logging.getLogger()
logger.addHandler(exim_handler)
```
