# dataclasses_fromdict

## Usage

``` py
from dataclasses import dataclass, asdict
from dataclasses_fromdict import from_dict

@dataclass
class Point:
    x: int
    y: int

assert from_dict(asdict(Point(10, 20)), Point) == Point(10, 20)
```

## Support

* generic list
* generic tuple
* generic var tuple
