
## Access the value from key
```python
from box import ConfigBox
# in dict() type we cannot cces using data.key
data = ConfigBox({"key": "value", "key1": "value1"})
# data acess method
>>> data.key
value

```

## Ensure annotation in parameter
`ensure_annotation` is decorator which **strongly(strictly)** ensure a singe data type is only passed through function
```python
from ensure import ensure_annotation

# without ensure_annotation
def get_product(x:int, y:  int):
    '''
    it works on integer passed as string
    >>> get_product("4", 2)
    44
    '''
    return x*y

@ensure_annotation
def get_product(x: int, y: int):
    '''
    it strictly only allowed integer datatype
    >>> get_product("4", 2)
    Error
    '''
    return x*y
```

  git config user.email "realsanjeev2@gmail.com"
  git config user.name "realsanjeev"