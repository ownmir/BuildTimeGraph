"""
Основний модуль Побудова тайм-графу
"""

# import common
import config
import datetime
from abc import ABC
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_protect
# from forms import PauseForm
import http.client
import urllib.parse

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
        """операція порівняння менше рівне"""
        return self.time <= other.time

    def __lt__(self, other):
        """операція порівняння менше"""
        return self.time < other.time

    def __sub__(self, other):
        """операція віднімання"""
        return self.time - other.time

    def __repr__(self):
        return "Point " + str(self._time)


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

    def __lt__(self, other):
        """оператор порівняння менше"""
        return self.length() < other.length()

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


# @csrf_protect
# def index(request):
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = PauseForm(request.POST)
#         if form.is_valid():
#             value_pause = form.cleaned_data["pause"]
#             return render(request, "result.html", {"value_pause": value_pause})
#     else:
#         form = PauseForm()
#     return render(request, "index.html", {"form": form})


if __name__ == "__main__":
    print("Початок")
    print("Time good", Point(1165615616551))
    line_segment1 = WorkLineSegment(Point(1165615616551), Point(1165615616552))
    line_segment1.set_type()
    print("Type", line_segment1.type_ls)

    # Результат
    timegraph = []

    # Input data
    # ==========

    # 1.	Timestamp початку
    begin_point = Point(1)
    # 2.	Чи час виконання в годинах, чи ні (inHours, boolean)
    in_hours = False
    #
    if in_hours:
        print("Duration in hours.")
        end_point = None
        # Тривалисть

    else:
        # 3 Timestamp закінчення
        end_point = Point(11)
        # Тривалисть
        duration = end_point - begin_point

    # --------------
    # optional input
    # --------------

    # 1.	Один, або декілька неробочих періодів (downtimes)
    # downtimes = [PauseLineSegment(Point(3), Point(5)), PauseLineSegment(Point(8), Point(9))]
    downtimes = []
    # 2.	Timestamp паузи
    # pause = None  # or pause = Point(3)  # or pause = Point(8)
    pause = Point(3)
    # 3.	Timestamp відновлення (resume)
    resume = None  # or  resume = Point(5)  # or resume = Point(9)
    # resume = Point(5)
    # =======
    if downtimes and pause is None and resume is None:
        print("Work with downtimes")
        # Робимо список точок
        point_list = []
        # Робимо кортеж типів відрізків: PAUSE - 0, WORK - 1
        (PAUSE, WORK) = (0, 1)
        mid_work_ls = WorkLineSegment(Point(begin_point.time), Point(end_point.time))
        last_ls = WorkLineSegment(Point(end_point.time - 1), Point(end_point.time))
        for ls in downtimes:
            mid_work_ls._B = ls._A
            point_list.append(("Work", mid_work_ls._A, mid_work_ls._B))
            point_list.append(("Pause", ls._A, ls._B))
            mid_work_ls._A = ls._B
            last_ls._A = ls._B
        point_list.append(("Work", last_ls._A, last_ls._B))
        print("point_list", point_list)

    elif not downtimes and pause and resume is None:
        print("Work with pause")
        point_list = [('Work', Point(1), Point(3)), ('Pause', Point(3), Point(5)), ('Work', Point(5), Point(8)),
                      ('Pause', Point(8), Point(9)), ('Work', Point(9), Point(11))]
        # Якщо пауза припадає на робочий період, то останній робочій період в кінцевому результаті (timegraph)
        # має закінчуватися на цьому timestamp.

        params = urllib.parse.urlencode(
            {'@pause': 4}
        )
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn = http.client.HTTPConnection("127.0.0.1", port=8080)
        conn.request("POST", "/cgi-bin/form.py", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)

        data = response.read()
        print(data)

        conn.close()
        for point_item in point_list:
            print(point_item[0], point_item[1], point_item[2])
            if point_item[0] == "Work" and pause <= point_item[2]:
                if pause < point_item[2]:
                    tuple_for_time_graph = ("Work", point_item[1], pause)
                    timegraph.append(tuple_for_time_graph)
                    break
            elif point_item[0] == "Pause" and pause <= point_item[2]:
                pass
            else:
                timegraph.append(point_item[2])
    elif not downtimes and pause is None and resume:
        print("Work with resume")

    print("Фініш")
