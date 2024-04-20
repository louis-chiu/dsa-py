from typing import Self, Sequence, TypeVar
T = TypeVar('T')


####################################
#           Static Array           #   
####################################
class Array(Sequence[T]):
  """
    Static array implementation in Python.
    
    Rules:
        1. Initialization will implicitly record the length and type of element.
        2. You need to complete the array operation.
            - Add element
                - in tail
                - in the middle
                - in uncontinuously position
                - array is full
            - Remove element
                - in tail
                - in any places
                - array is empty
            - Search element
            - Modify element
  """
  def __init__(self, *args: T) -> None:
    self.element_types: set[T] = {type(e) for e in args}
    if len(self.element_types) > 2:
      raise TypeError('Array allows elements to have only one type.')

    self.values: list[T] = [*args]
    self.element_type: T = next(filter(lambda e: e is not None ,self.element_types))
    self.init_size: int = len(self.values)
    self.curr_size: int = len(self.values)

  def __str__(self) -> str:
    return self.values.__str__()
  
  def __repr__(self) -> str:
    return self.values.__repr__()

  def __len__(self) -> int:
    return self.init_size
  
  def __getitem__(self, index: int) -> T:
    if index > self.curr_size:
      raise IndexError('Cannot access discontinuous position.')

    return self.values.__getitem__(index)

  def __setitem__(self, index, value) -> None:
    if type(value) != self.element_type:
      raise TypeError(f'{value} is not a {self.element_type.__name__}')
    elif index > self.curr_size:
      raise IndexError('Cannot access discontinuous position.')
    
    self.values.__setitem__(index, value)

  def append(self, element: T) -> Self:
    if type(element) != self.element_type:
      raise TypeError(f'Cannot append element of type {type(element).__name__} is not a {self.element_type.__name__} type.')
    elif self.curr_size >= len(self):
      raise IndexError(f'Array is full. Size is {len(self)}.')
    
    self.values[self.curr_size] = element
    self.curr_size += 1
    return Array(*self.values)
  
  def insert(self, position: int, element: T) -> Self:
    if type(element) != self.element_type:
      raise TypeError(f'Cannot append element of type {type(element).__name__} is not a {self.element_type.__name__} type.')
    elif self.curr_size >= len(self):
      raise IndexError(f'Array is full. Size is {len(self)}.')
    elif position > self.curr_size:
      raise IndexError('Cannot access discontinuous position.')
    elif position == (self.curr_size - 1):
      return self.append(element)

    self.values[position + 1:self.curr_size + 1] = self.values[position:self.curr_size]
    self.values[position] = element
    self.curr_size += 1
    return Array(*self.values)

  def pop(self):
    if self.curr_size == 0:
      raise IndexError('Array is empty')
    
    self.values[self.curr_size - 1] = None
    self.curr_size -= 1
    return Array(*self.values)

  def remove(self, position):
    if self.curr_size == 0:
      raise IndexError('Array is empty')
    elif 0 > position:
      raise IndexError('position cannot be negative.')
    elif position >= len(self):
      raise IndexError('out of index')
    elif position == (len(self) - 1):
      return self.pop()
    
    self.values[position:self.curr_size - 1] = self.values[position + 1:self.curr_size]
    self.values[self.curr_size - 1] = None
    self.curr_size -= 1
    return Array(*self.values)
    





