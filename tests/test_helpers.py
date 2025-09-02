"""Create and test some helper functions for book_cataloguing tests to use."""

import unittest


def double_chars(string):
    result = ""

    for char in string:
        result = "".join((
            result,
            char,
            char
        ))

    return result


def undouble_chars(string):
    result = ""

    for i, char in enumerate(string):
        if not i % 2:
            result = "".join((result, char))

    return result


class HelperFunctionsTest(unittest.TestCase):
    def test_double_and_undouble_chars(self):
        data = (
            ("", ""),
            ("cat", "ccaatt"),
            (" ~HI!", "  ~~HHII!!")
        )
        for in_, out in data:
            self.assertEqual(double_chars(in_), out)
            self.assertEqual(undouble_chars(out), in_)


if __name__ == "__main__":
    unittest.main()
