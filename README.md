# lazysequence
A mutable sequence that lazily loads values. Allows for a cleaner use of, for example, paginated resources that you would want to index.

It has the exact same api a list allowing it to be used everywhere you'd use a list without any drawbacks.

# usage and examples
LazySequence takes in any iterable
```py
>>> x = LazySequence(i for i in range(7))
>>> x
LazySequence([...])
```

It loads only the exact amount of items it needs, here we need only 5
```py
>>> x[2]
2
>>> x[4] = 0
>>> x
LazySequence([0, 1, 2, 3, 0, ...])
```

Appending just adds the item to the internal iterator, it does not actually get loaded
```py
>>> x.append(100)
>>> x
LazySequence([0, 1, 2, 3, 0, ...])
```

Getting an item from the back loads the entire iterator
```py
>>> x[-3]
5
>>> x
LazySequence([0, 1, 2, 3, 0, 5, 6, 100])
```

After that appended items are immediatelly evaluated
```py
>>> x.append(500)
>>> x
LazySequence([0, 1, 2, 3, 0, 5, 6, 100, 500])
```

Although extended items are not loaded
```py
>>> x.extend(i for i in (-1, -2, -3, -4))
>>> x
LazySequence([0, 1, 2, 3, 0, 5, 6, 100, 500, ...])
```

Getting the index of an item also does not evaluate more than it needs
```py
>>> x.index(-2)
10
>>> x
LazySequence([0, 1, 2, 3, 0, 5, 6, 100, 500, -1, -2, ...])
```

Getting the length evaluates the iterator, there is no way around that
```py
>>> len(x)
13
>>> x
LazySequence([0, 1, 2, 3, 0, 5, 6, 100, 500, -1, -2, -3, -4])
```

Passing in a sequence evaluates all values beforehand
```py
>>> LazySequence("abcde")
LazySqequence(['a', 'b', 'c', 'd', 'e'])
```

Trying to get to the end of an infinite iterator raises an error
```py
>>> from itertools import count
>>> len(LazySequence(count()))
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    len(LazySequence(count()))
MemoryError: Cannot exhaust an infinite iterator
```