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

    def length(self):
        """довжина відрізка у секундах"""
        return self._B.time - self._A.time

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
    print("Time good", Point(1165615616551))
    line_segment1 = WorkLineSegment(Point(1165615616551), Point(1165615616552))
    line_segment1.set_type()
    print("Type", line_segment1.type_ls)

    # Input data
    # ==========

    # 1.	Timestamp початку
    begin_point = 1
    # 2.	Чи час виконання в годинах, чи ні (inHours, boolean)
    in_hours = False
    #
    if in_hours:
        print("Duration in hours.")
        end_point = None
        # Тривалисть

    else:
        # 3 Timestamp закінчення
        end_point = 10
        # Тривалисть
        duration = end_point - begin_point

    # --------------
    # optional input
    # --------------

    # 1.	Один, або декілька неробочих періодів (downtimes)
    downtimes = [PauseLineSegment(Point(3), Point(5)), PauseLineSegment(Point(8), Point(9))]
    # 2.	Timestamp паузи
    pause = None  # or pause = Point(3)  # or pause = Point(8)
    # 3.	Timestamp відновлення (resume)
    resume = None  # or  resume = Point(5)  # or resume = Point(9)
    # =======
    if downtimes and pause is None and resume is None:
        print("Work with downtimes")
    elif not downtimes and pause and resume is None:
        print("Work with pause")
    elif not downtimes and pause is None and resume:
        print("Work with resume")
    res = []
    print("Фініш")
