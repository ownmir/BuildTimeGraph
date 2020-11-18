import unittest
from main import *  # Point, LineSegment, LineSegment, PauseLineSegment


class PointTestCase(unittest.TestCase):

    def testValue(self):
        arg = -1
        self.assertRaises(ValueError, Point, arg)

    def testLETrue(self):
        self.assertTrue(Point(1) <= Point(2))

    def testLEFalse(self):
        self.assertFalse(Point(2) <= Point(1))

    def testType(self):
        """тест на тип аргументів в класі"""
        self.assertRaises(TypeError, Point, "fsa")
    
    def testArgs(self):
        """тест на кількість аргументів в класі"""
        self.assertRaises(TypeError, Point, "fsa", "fds")


class LineSegmentTestCase(unittest.TestCase):

    def testInt(self):
        """тест на тип аргументів в класі"""
        self.assertRaises(TypeError, LineSegment, ("fsa", "fds"))

    def testArgs(self):
        """тест на кількість аргументів в класі"""
        self.assertRaises(TypeError, LineSegment, ("fsa", "fds", "tre"))

    def testValue(self):
        argss = (Point(2), Point(1))
        self.assertRaises(ValueError, LineSegment, Point(2), Point(1))
        args = (1, 2)
        self.assertRaises(TypeError, LineSegment, args)

    def testNotImplemented(self):
        try:
            LineSegment(Point(1), Point(2)).set_type()
        except AttributeError:
            print("testNotImplemented is OK")
        


if __name__ == '__main__':
    unittest.main()
