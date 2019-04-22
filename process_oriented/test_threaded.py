import unittest
from threaded import *

SEED = 42
np.random.seed(SEED)


class TestFutureEventList(unittest.TestCase):

    def test_push(self):
        fel = FutureEventList()
        self.assertEqual([], fel.data)

        fel.push("3", 3)
        fel.push("2", 2)
        fel.push("4", 4)
        fel.push("5", 5)

        first = (2, "2")
        self.assertEqual(fel.data[0], first)


    def test_pop(self):
        fel = FutureEventList()
        self.assertEqual([], fel.data)

        fel.push("3", 3)
        fel.push("2", 2)
        fel.push("4", 4)
        fel.push("5", 5)

        expected = (2, "2")
        actual = fel.pop()
        self.assertEqual(expected, actual)

        first = (3, "3")
        self.assertEqual(fel.data[0], first)

        expected = (3, "3")
        actual = fel.pop()
        self.assertEqual(expected, actual)

        expected = (4, "4")
        actual = fel.pop()
        self.assertEqual(expected, actual)

        expected = (5, "5")
        actual = fel.pop()
        self.assertEqual(expected, actual)


    def test_peek(self):
        fel = FutureEventList()
        fel.push("3", 3)
        fel.push("2", 2)
        fel.push("4", 4)
        fel.push("5", 5)

        expected = (2, "2")
        actual = fel.peek()
        self.assertEqual(expected, actual)
        _ = fel.pop()  # Throw away

        first = (3, "3")
        self.assertEqual(fel.data[0], first)

        expected = (3, "3")
        actual = fel.peek()
        self.assertEqual(expected, actual)

        # Do it again to ensure peek doesn't destroy any data.
        expected = (3, "3")
        actual = fel.peek()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
