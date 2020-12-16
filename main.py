"""
Основний модуль Побудова тайм-графу
"""

# import common
import config
import datetime
import sys
import os
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


def hand_exit(json_str, code):
    
    if code < 40 or code > 69:
        print(json_str)
    sys.exit(code)
    # try:
    #     sys.exit(code)
    # except SystemExit:
    #     pass


if __name__ == "__main__":
    if config.DEBUG:
        print("Початок")
    else:
        pass

    # 
    error_code = 0
    # Результат
    timegraph = []

    # Input data
    # ==========

    # 1.	Timestamp початку
    # begin_point = Point(1)
    try:
        arg_begin_point = sys.argv[1]
        try:
            begin_point = json.loads(arg_begin_point)
        except json.JSONDecodeError:

            if config.DEBUG:
                begin_point = 1
                print("Error! Wrong argument 1")
            else:
                begin_point = None
                error_code = 11
                hand_exit("""["Error", "Wrong argument 1"]""", 11)
    except IndexError:
        if config.DEBUG:
            arg_begin_point = """1"""
            begin_point = json.loads(arg_begin_point)
        else:
            begin_point = None
            error_code = 12
            hand_exit("""["Error", "No argument 1"]""", 12)
    #
    if config.DEBUG:
        if begin_point:
            print("begin_point", begin_point)
    # 2.	Чи час виконання в годинах, чи ні (inHours, boolean)
    try:
        arg_in_hours = sys.argv[2]
        try:
            in_hours = json.loads(arg_in_hours)
        except json.JSONDecodeError:
            if config.DEBUG:
                print("Error! Wrong argument 2")
                in_hours = False
            else:
                in_hours = False
                error_code = 21
                hand_exit("""["Error", "Wrong argument 2"]""", 21)

    except IndexError:
        if config.DEBUG:
            in_hours = False
        else:
            in_hours = False
            hand_exit("""["Error", "No argument 2"]""", 22)
    if in_hours:
        if config.DEBUG:
            print("Duration in hours.")
        end_point = None
        # Тривалисть

    else:
        # 3 Timestamp закінчення
        try:
            arg_end_point = sys.argv[3]
            try:
                end_point = json.loads(arg_end_point)
            except json.JSONDecodeError:
                if config.DEBUG:
                    print("Error! Wrong argument 3", arg_end_point)
                else:
                    error_code = 31
                    hand_exit("""["Error", "Wrong argument 3"]""", 31)
        except IndexError:
            if config.DEBUG:
                print("Error! No argument 3")
                end_point = 11
            else:
                hand_exit("""["Error", "No argument 3"]""", 32)
            # return """['Error', 'No argument 3']"""
        # end_point = 11
        # Тривалисть
        try:
            duration = end_point - begin_point
        except NameError:
            pass

    # --------------
    # optional input
    # --------------
    if config.DEBUG:
        print("sys.argv", sys.argv)
    # 1.	Один, або декілька неробочих періодів (downtimes)
    try:
        # start python -i main.py 1 false 11 [[\"Pause\",3,5],[\"Pause\",8,9]] null null
        # Notepad++:
        # D:\Python377-32\python.exe -i "$(FULL_CURRENT_PATH)" "1" "false" "11" "[[\"Pause\",3,5],[\"Pause\",8,9]]" "null" "null"
        arg_downtimes = sys.argv[4]
        if config.DEBUG:
            print('arg_downtimes', arg_downtimes, 'type', type(arg_downtimes))
        for_load_downtimes = arg_downtimes
        try:
            downtimes = json.loads(for_load_downtimes)
        except json.JSONDecodeError:
            downtimes = None
            if config.DEBUG:
                print("Error! Wrong argument 4")
            else:
                error_code = 41
                hand_exit("""["Error", "Wrong argument 4"]""", 41)
    except IndexError:
        if config.DEBUG:
            for_load_downtimes = """[ ["Pause", 3, 5], ["Pause", 8, 9] ]"""
            print("Error! No argument 4! Using", for_load_downtimes)
            try:
                downtimes = json.loads(for_load_downtimes)
            except json.JSONDecodeError:
                downtimes = None
                if downtimes:
                    pass
                if config.DEBUG:
                    print("Error! Wrong argument 4!")
                else:
                    error_code = 41
                    hand_exit("""["Error", "Wrong argument 4"]""", 41)
        else:
            # TODO: что делать, если не заданы 4, 5, 6?
            downtimes = None
            error_code = 42
            hand_exit("""["Error", "No argument 4"]""", 42)
    try:
        arg_pause = sys.argv[5]
        try:
            pause = json.loads(arg_pause)
            if config.DEBUG:
                print('pause', pause, 'type', type(pause))
        except json.JSONDecodeError as pause_error:
            pause = None
            if config.DEBUG:
                print("Error in loads JSON pause", pause_error)
            else:
                error_code = 51
                hand_exit("""["Error", "Wrong argument 5"]""", 51)
    except IndexError:
        pause = None
        if config.DEBUG:
            pass
        else:
            # TODO: что делать, если не заданы 4, 5, 6?
            error_code = 52
            hand_exit("""["Error", "No argument 5"]""", 52)
    try:
        arg_resume = sys.argv[6]
        try:
            resume = json.loads(arg_resume)
            if config.DEBUG:
                print('resume', resume, 'type', type(resume))
        except json.JSONDecodeError as resume_error:
            resume = None
            if config.DEBUG:
                print("Error in loads JSON resume", resume_error)
            else:
                error_code = 61
                hand_exit("""["Error", "Wrong argument 6"]""", 61)
    except IndexError:
        resume = None
        if config.DEBUG:
            pass
        else:
            # TODO: что делать, если не заданы 4, 5, 6?
            error_code = 62
            hand_exit("""["Error", "No argument 6"]""", 62)
        # for_load_downtimes = '{"PauseLineSegment1": {"Point1": {"time": 3}, "Point2": {"time": 5}}, ' \
        #                      '"PauseLineSegment2": {"Point1": {"time": 8}, "Point2": {"time": 9}}}'
    # только один из 4-го, 5, 6 параметров могут быть определены (bool(x) ^ bool(y) ^ bool(z)) and not (bx == by == bz)
    # ^ - исключающее или
    if not ((bool(downtimes) ^ bool(pause) ^ bool(resume)) and not (bool(downtimes) == bool(pause) == bool(resume))):
        if config.DEBUG:
            print("Only one of 4, 5, 6 parameters can be defined")
        else:
            error_code = 71
            hand_exit("""["Error", "Only one of 4, 5, 6 parameters can be defined"]""", 71)
    # downtimes = [PauseLineSegment(Point(3), Point(5)), PauseLineSegment(Point(8), Point(9))]
    ## downtimes = []
    # print("for_load_downtimes[19]", for_load_downtimes[10:19])
    ## downtimes_j = json.loads(for_load_downtimes)
    ## print("load from json", downtimes_j, type(downtimes_j))
    # {'PauseLineSegment1': {'Point1': {'time': 3}, 'Point2': {'time': 5}}, 'PauseLineSegment2': {'Point1': {'time': 8}, 'Point2': {'time': 9}}}
    #pause_time_list = []
    # проход по словарю несколько паузлайнсегмент
    # for pls_key, points in downtimes_j.items():
    #     print("pls_key", pls_key, "pls_value", points)
    #     # проход по словарю 2 поинта
    #     for key, value in points.items():
    #         print("key", key, "value", value, "value[time]", value["time"])
    #         # pause_time_list.append(value["time"])  # tuple(key, value["time"])
    #         pause_time_list.append((key, value["time"],))  # tuple(key, value["time"])
    # print("pause_time_list", pause_time_list)
    # downtimes2 = []
    # for pause_time in pause_time_list:
    #     print("pause_time", pause_time)

        # downtimes2.append(PauseLineSegment(Point(pause_time[0][1]), Point(pause_time[1][1])))

    # print("downtimes2", downtimes2)
    # 2.	Timestamp паузи
    # pause = None  # or pause = 3 Point(3)  # or pause = 8 Point(8)
    # pause = Point(6)
    # pause = 6
    # 3.	Timestamp відновлення (resume)
    # resume = None  # or  resume = Point(5)  # or resume = Point(9)
    # resume = Point(10)
    # resume = 10
    # =======
    if downtimes and pause is None and resume is None:
        if config.DEBUG:
            print("Work with downtimes")
        # Робимо список точок
        point_list = []
        mid_work_ls = ["Work", begin_point, end_point]
        last_ls = ["Work", (end_point - 1), end_point]
        # [['Pause', 3, 5], ['Pause', 8, 9]]
        for ls in downtimes:
            # mid_work_ls._B = ls._A
            mid_work_ls[2] = ls[1]
            # point_list.append(("Work", mid_work_ls._A, mid_work_ls._B))
            point_list.append(('Work', mid_work_ls[1], mid_work_ls[2]))
            # point_list.append(("Pause", ls._A, ls._B))
            point_list.append(('Pause', ls[1], ls[2]))
            # mid_work_ls._A = ls._B
            mid_work_ls[1] = ls[2]
            # last_ls._A = ls._B
            last_ls[1] = ls[2]
        # point_list.append(("Work", last_ls._A, last_ls._B))
        point_list.append(('Work', last_ls[1], last_ls[2]))
        if config.DEBUG:
            print("point_list", point_list)
        # point_list_json = json.dumps(point_list)
        timegraph = json.dumps(point_list)
        if config.DEBUG:
            print("timegraph", timegraph)

    elif not downtimes and pause and resume is None:
        if config.DEBUG:
            print("Work with pause", pause)
        point_list = [['Work', 1, 3], ['Pause', 3, 5], ['Work', 5, 8], ['Pause', 8, 9], ['Work', 9, 11]]
        # for_dump_pause = """[['Work', 1, 3], ['Pause', 3, 5], ['Work', 5, 8], ['Pause', 8, 9], ['Work', 9, 11]]"""
        
        # Якщо пауза припадає на робочий період, то останній робочій період в кінцевому результаті (timegraph)
        # має закінчуватися на цьому timestamp.

        params = urllib.parse.urlencode(
            {'pause': pause}
        )
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn = http.client.HTTPConnection("127.0.0.1", port=8080)
        conn.request("POST", "/cgi-bin/form.py", params, headers)
        response = conn.getresponse()
        if config.DEBUG:
            print(response.status, response.reason)

        data = response.read()
        if config.DEBUG:
            print(data)

        conn.close()
        for point_item in point_list:
            if config.DEBUG:
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
        if config.DEBUG:
            print("Time-graph", timegraph)
            print(json.dumps(timegraph, indent=2, cls=PointEncoder))
    elif not downtimes and pause is None and resume:
        if config.DEBUG:
            print("Work with resume", resume)
        point_list = [['Work', 1, 3], ['Pause', 3, 5], ['Work', 5, 8], ['Pause', 8, 9], ['Work', 9, 11]]
        # for_load_resume = '[["Work", 1, 3], ["Pause", 3, 5], ["Work", 5, 8], ["Pause", 8, 9], ["Work", 9, 11]]'
        # point_list = json.loads(for_load_resume)
        for point_item in point_list:
            if config.DEBUG:
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
        if config.DEBUG:
            print("Time-graph", timegraph)
        # print(json.dumps(timegraph, indent=2, cls=PointEncoder))
    if config.DEBUG:
        print("Фініш")
    else:
        if error_code not in (11, 12, 21, 22, 31, 32, 41, 51, 61, 71):
            hand_exit(json.dumps(timegraph), 0)
        # print("Time-graph", timegraph)
