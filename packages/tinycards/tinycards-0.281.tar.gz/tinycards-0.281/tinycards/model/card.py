from uuid import uuid4

from .concept import Concept
from .fact import Fact
from .side import Side


def current_timestamp():
    """Get current time in milliseconds.

    While Python usually works in seconds, JavaScript uses milliseconds and
    we want to be compatible.
    """
    from time import time
    return int(time()) * 1000


class Card(object):
    """Data class for an Tinycards card entity."""

    def __init__(self,
                 front,
                 back,
                 card_id=None,
                 creation_timestamp=None):
        """Initialize a new instance of the Card class."""
        self.id = card_id if card_id else str(uuid4())

        self.creation_timestamp = creation_timestamp or current_timestamp()

        # While Tinycards originally uses a (2 element) tuple to
        # represent both sides, we chose to go with a more
        # semantic naming here.
        if isinstance(front, Side):
            self.front = front
        elif isinstance(front, str):
            self.front = Side(concepts=Concept(Fact(front)))
        else:
            raise ValueError("Front property can only be of type Side")
        if isinstance(back, Side):
            self.back = back
        elif isinstance(back, str):
            self.back = Side(concepts=Concept(Fact(back)))
        else:
            raise ValueError("Back property can only be of type Side")

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
