# fca-math

Formal Concept Analysis (FCA) mathematical library for Python.

## Installation

```bash
poetry install
```

## Usage

```python
from fca_math import Context

# Create a context with 3 objects and 4 attributes
kk = Context(3, 4)
kk.make_incident(1, 2)
print(kk)
```
