import itertools
from collections.abc import MutableSequence
from typing import Generic, Iterable, Iterator, List, Sequence, TypeVar

__all__ = ['IteratorSequence']

T = TypeVar('T')

class LazySequence(Generic[T], MutableSequence[T]):
    """A mutable sequence that lazily loads values."""
    iterator: Iterator[T]
    evaluated: List[T]
    exhausted: bool = False
    MAX_SIZE = 0xffff
    
    def __init__(self, iterable: Iterable[T]) -> None:
        """A mutable sequence that lazily loads values.
        
        Takes in an iterable which will be lazily loaded, 
        if a sequence is passed in then all values are loaded in advance.
        """
        if not isinstance(iterable, Sequence):
            self.iterator = iter(iterable)
            self.evaluated = []
        else:
            self.iterator = iter(())
            self.evaluated = list(iterable)
            self.exhausted = True
    
    def __repr__(self) -> str:
        s = ', '.join(map(repr, self.evaluated))
        if s == '':
            s = '...'
        elif not self.exhausted:
            s += ', ...'
        return f"{type(self).__name__}([{s}])"
    
    def _exhaust(self) -> None:
        """Exhausts the entire iterator"""
        for i in self.iterator:
            self.evaluated.append(i)
            if len(self.evaluated) >= self.MAX_SIZE:
                raise MemoryError("Cannot exhaust an infinite iterator")
        
        self.exhausted = True
    
    def _seek(self, index: int) -> T:
        """Exhausts the iterator until index is reached"""
        if index < 0:
            self._exhaust()
            return self.evaluated[index]

        while len(self.evaluated) <= index:
           if next(self, None) is None:
               self.exhausted = True
               raise IndexError('index out of range')
        
        return self.evaluated[index]

    def __iter__(self) -> Iterator[T]:
        """Returns a separate iterator that yields all values"""
        yield from self.evaluated
        while True:
            try:
                yield next(self)
            except StopIteration:
                return

    def __next__(self) -> T:
        """Yields next value and stores it in sequence"""
        x = next(self.iterator)
        self.evaluated.append(x)
        return x

    def __len__(self) -> int:
        self._exhaust()
        return len(self.evaluated)

    def __getitem__(self, index: int) -> T:
        return self._seek(index)

    def __setitem__(self, index: int, item: T) -> None:
        self._seek(index)
        self.evaluated[index] = item
    
    def __delitem__(self, index: int) -> None:
        self._seek(index)
        del self.evaluated[index]
    
    def insert(self, index: int, value: T) -> None:
        self._seek(index)
        self.evaluated.insert(index, value)
    
    def append(self, value: T) -> None:
        if self.exhausted:
            self.evaluated.append(value)
        else:
            self.extend([value])

    def extend(self, values: Iterable[T]) -> None:
        self.iterator = itertools.chain(self.iterator, values)
        self.exhausted = False
