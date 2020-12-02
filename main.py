"""
Основний модуль Побудова тайм-графу
"""

# import common
import config
import datetime
import sys
from abc import ABC
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_protect
# from forms import PauseForm
import http.client
import urllib.parse
import json


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

    def get_json(self):
        return json.dumps({"time": self.time})


class PointEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Point):
            return {"time": obj.time}
        return json.JSONEncoder.default(self, obj)


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

    def get_json(self):
        """Представлення в json відрізка роботи"""
        o = '{'
        cl = '}'
        return json.dumps('{0}"type_ls": "Work", "A": {1}, "B": {2}{3}'.format(o, self._A.get_json(),
                                                                                self._B.get_json(), cl))


class WorkLineSegmentEncoder(json.JSONEncoder):
    def for_point(self, point):
        return {"time": point.time}

    def default(self, obj):
        if isinstance(obj, WorkLineSegment):
            return {"type_ls": "Work", "A": self.for_point(obj._A), "B": self.for_point(obj._B)}
        return json.JSONEncoder.default(self, obj)


class PauseLineSegment(LineSegment):
    """Відрізок паузи"""

    def set_type(self):
        self.type_ls = "Pause"

    def get_json(self):
        """Представлення в json відрізка паузи"""
        o = '{'
        cl = '}'
        return json.dumps('{0}"type_ls": "Pause", "A": {1}, "B": {2}{3}'.format(o, self._A.get_json(),
                                                                                self._B.get_json(), cl))


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


def objects_from_json(par_json):
    res = json.loads(par_json)
    print(res)
    return res


def downtimes_do(par_json):
    downtimes = objects_from_json(par_json)


if __name__ == "__main__":
    print("Початок")
    print("Time good", Point(1165615616551))
    line_segment1 = WorkLineSegment(Point(1165615616551), Point(1165615616552))
    line_segment1.set_type()
    print("Type", line_segment1.type_ls)
    # print("line_segment1 json.dumps", line_segment1.get_json())
    # print("line_segment1 json.dumps with WorkLineSegmentEncoder", json.dumps(line_segment1, indent=2, cls=WorkLineSegmentEncoder))

    # Результат
    timegraph = []

    # Input data
    # ==========

    # 1.	Timestamp початку
    # begin_point = Point(1)
    begin_point = Point(1)
    print("begin_point json.dumps", begin_point.get_json())
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
    try:
        arg_downtimes = sys.argv[1]
        for_load_downtimes = arg_downtimes
    except IndexError:
        for_load_downtimes = '{"PauseLineSegment1": {"Point1": {"time": 3}, "Point2": {"time": 5}}, ' \
                             '"PauseLineSegment2": {"Point1": {"time": 8}, "Point2": {"time": 9}}}'
    downtimes = [PauseLineSegment(Point(3), Point(5)), PauseLineSegment(Point(8), Point(9))]
    # downtimes = []
    print("for_load_downtimes[19]", for_load_downtimes[10:19])
    downtimes_j = json.loads(for_load_downtimes)
    print("load from json", downtimes_j, type(downtimes_j))
    # {'PauseLineSegment1': {'Point1': {'time': 3}, 'Point2': {'time': 5}}, 'PauseLineSegment2': {'Point1': {'time': 8}, 'Point2': {'time': 9}}}
    pause_time_list = []
    # проход по словарю несколько паузлайнсегмент
    for pls_key, points in downtimes_j.items():
        print("pls_key", pls_key, "pls_value", points)
        # проход по словарю 2 поинта
        for key, value in points.items():
            print("key", key, "value", value, "value[time]", value["time"])
            pause_time_list.append(value["time"])

    print("pause_time_list", pause_time_list)
    # 2.	Timestamp паузи
    pause = None  # or pause = Point(3)  # or pause = Point(8)
    # pause = Point(6)
    # 3.	Timestamp відновлення (resume)
    resume = None  # or  resume = Point(5)  # or resume = Point(9)
    # resume = Point(10)
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
            {'pause': pause.time}
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
                else:
                    timegraph.append(point_item)
            elif point_item[0] == "Pause" and pause <= point_item[2]:
                # Якщо пауза припадає на неробочий період, то останній робочій період в timegraph має бути той,
                # який передував цьому неробочому періоду.
                tuple_for_time_graph = ("Pause", point_item[1], pause)
                timegraph.append(tuple_for_time_graph)
                break
            else:
                timegraph.append(point_item)
        print("Time-graph", timegraph)
        print(json.dumps(timegraph, indent=2, cls=PointEncoder))
    elif not downtimes and pause is None and resume:
        print("Work with resume")
        point_list = [('Work', Point(1), Point(3)), ('Pause', Point(3), Point(5)), ('Work', Point(5), Point(8)),
                      ('Pause', Point(8), Point(9)), ('Work', Point(9), Point(11))]
        for point_item in point_list:
            print(point_item[0], point_item[1], point_item[2])
            if point_item[0] == "Work" and resume <= point_item[2]:
                if resume < point_item[2]:
                    tuple_for_time_graph = ("Work", point_item[1], resume)
                    timegraph.append(tuple_for_time_graph)
                    break
                else:
                    timegraph.append(point_item)
            elif point_item[0] == "Pause" and resume <= point_item[2]:
                if resume < point_item[2]:
                    tuple_for_time_graph = ("Pause", point_item[1], resume)
                    timegraph.append(tuple_for_time_graph)
                    break
                else:
                    timegraph.append(point_item)
            else:
                timegraph.append(point_item)
        print("Time-graph", timegraph)
        # print(json.dumps(timegraph, indent=2, cls=PointEncoder))
    print("Фініш")
