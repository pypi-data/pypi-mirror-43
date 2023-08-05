# Pyvent

Pyvent is a dead-simple IPC to use that uses ZMQ and PyDispatcher under the hood.

## Usage

### Basic

```python
# script1.py
import pyvent

@pyvent.connect('order-food')
def order(food, drink='water'):
  print(f'You ordered {food} and {drink}!')
```


```python
# script2.py
import pyvent

pyvent.send('order-food', food='sushi', drink='sake')
```

```shell
$ python3 script1.py &
$ python3 script2.py
> You ordered sushi and sake!
```


