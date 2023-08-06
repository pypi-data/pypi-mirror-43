# Jivago-Streams
[![Build Status](https://travis-ci.com/jivago-python/jivago-streams.svg?branch=master)](https://travis-ci.com/jivago-python/jivago-streams)
[![codecov](https://codecov.io/gh/jivago-python/jivago-streams/branch/master/graph/badge.svg)](https://codecov.io/gh/jivago-python/jivago-streams)

Jivago-Streams brings the ability to chain functional-style operations on collections. 
This package provides a single class (`Stream`), which is extracted from the Jivago web framework.
Note that *jivago-streams* can be used independently from the Jivago web framework.

```python
from jivago_streams import Stream

# Result : [4, 16, 36]
square_of_even_numbers = Stream([1, 2, 3, 4, 5, 6]) \
    .filter(lambda x: x % 2 == 0) \
    .map(lambda x: x ** 2) \
    .toList()
```

## Installation
`pip install jivago-streams`

## Documentation
The documentation is available at [https://docs.jivago.io](https://docs.jivago.io/en/develop/streams/index.html).
