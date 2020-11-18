"""
Основний модуль Побудова тайм-графу
"""

# import common
import config
import datetime
from abc import ABC

# common.ee()

class Point(ABC):
    """
    timestamp в секундах
    """
    def __init__(self, time):
        if not isinstance(time, int):
            raise TypeError('Arg must be integer.')
        if time > 0:
            self._time = time
        else:
            raise ValueError('Arg must be positive.')

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, time):
        if time > 0:
            self._time = time
        else:
            raise ValueError('Arg must be positive.')

    def __le__(self, other):
        """оператор порівняння менше рівне"""
        return self.time <= other.time



class LineSegment(ABC):
    """ Абстрактний клас відрізка"""

    type_ls = ""
    def __init__(self, A, B):
        if (not isinstance(A, Point)) or (not isinstance(B, Point)):
            raise TypeError('Args must be Point.')
        if A.time > 0 and B.time > 0 and A <= B:
            self._A = A
            self._B = B
        else:
            raise ValueError("Begin, End, End - Begin  must be positive.")

    def length():
        """довжина відрізка у секундах"""
        return B.time - A.time

    def __le__(self, other):
        """оператор порівняння менше рівне"""
        return self.length() <= other.length()

    def set_type(self):
        """задати тип відрізка - фабричний метод"""
        raise AttributeError('Not Implemented type')


class WorkLineSegment(LineSegment):
    """Відрізок роботи"""
    def set_type(self):
        self.type_ls = "Work"

class PauseLineSegment(LineSegment):
    """Відрізок паузи"""
    def set_type(self):
        self.type_ls = "Pause"



if __name__ == "__main__":
    print("Початок")
    # config.time_graph =
    print("Time good", Point(1165615616551))
    # print("Time bad", Point("fds"))
    # print("Time bad", Point(-1165615616551))
    line_segment1 = WorkLineSegment(Point(1165615616551), Point(1165615616552))
    line_segment1.set_type()
    print("Type", line_segment1.type_ls)
##    line_segment2 = LineSegment(Point(1), Point(2))
##    line_segment2.set_type()
    print("Фініш")
