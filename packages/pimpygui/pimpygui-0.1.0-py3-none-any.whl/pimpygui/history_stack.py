from typing import Any, Iterable, Iterator


class HistoryStack(object):
    """Contains a stack and an index and provides go backwards / forwards functionality."""

    def __init__(self, history: Iterable = None, current_index: int = -1) -> None:
        """Creates a stack that contains the given elements. The given index is clipped to the interval
        [-1, len(history)-1]."""
        if history is None:
            history = []
        current_index = max(current_index, -1)
        current_index = min(current_index, len(history) - 1)
        self._history = list(history)
        self._current_index = current_index

    def __iter__(self) -> Iterator[Any]:
        """Returns an iterator to the elements."""
        return iter(self._history)

    def __len__(self) -> int:
        """Returns the number of elements in this history."""
        return len(self._history)

    def get_current_index(self) -> int:
        """Returns the current index."""
        return self._current_index

    def add(self, obj: Any) -> None:
        """Adds the given object after the current object and removes all following objects."""
        self._history = self._history[:self._current_index+1]
        self._history.append(obj)
        self._current_index = len(self._history) - 1

    def get(self) -> Any:
        """Returns the current object, or None if there is no current object."""
        if 0 <= self._current_index < len(self._history):
            return self._history[self._current_index]
        return None

    def can_go_backwards(self) -> bool:
        """Returns True if go_backwards() can actually do something useful."""
        return self._current_index >= 0

    def can_go_forwards(self) -> bool:
        """Returns True if go_forwards() can actually do something useful."""
        return self._current_index + 1 < len(self._history)

    def go_backwards(self) -> None:
        """Decrements the current index."""
        if self.can_go_backwards():
            self._current_index -= 1

    def go_forwards(self) -> None:
        """Increments the current index."""
        if self.can_go_forwards():
            self._current_index += 1
