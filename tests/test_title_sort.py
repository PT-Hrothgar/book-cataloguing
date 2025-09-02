"""Test the function book_cataloguing.title_sort()"""

import book_cataloguing as mod
import random
import unittest

from test_helpers import double_chars, undouble_chars


class TitleSortTest(unittest.TestCase):
    def test_title_sort(self):
        titles = "meet the austins", "meet thee austins"
        self.assertEqual(
            mod.title_sort(titles),
            ["meet the austins", "meet thee austins"]
        )
        titles = (
            "TREasure islanD",
            "the book of three",
            "th.e +Canterbur*y (tal;es"
        )
        self.assertEqual(
            mod.title_sort(titles),
            [
                "the book of three",
                "th.e +Canterbur*y (tal;es",
                "TREasure islanD"
            ]
        )

    def test_title_sort_with_key_and_reverse(self):
        output = [
            ("The Bible of Illuminated Letters: A Treasury of Decorative Calli"
             "graphy"),
            "Book of North American Birds",
            "The Complete Book of Calligraphy",
            "The French Twins",
            "Idylls of the King",
            "Mastering Copperplate Calligraphy: A Step-by-Step Manual",
            "Medieval Calligraphy: Its History and Technique",
            "Nancy Kelsey",
            "Sylvester and the Magic Pebble",
            "The Xanadu Adventure"
        ]
        titles = output.copy()
        for i in range(15):
            random.shuffle(titles)
            self.assertEqual(mod.title_sort(titles), output)
            self.assertEqual(
                mod.title_sort(
                    titles,
                    reverse=True
                ),
                list(reversed(output))
            )

        for i, (title, out) in enumerate(zip(titles, output)):
            titles[i] = double_chars(title)
            output[i] = double_chars(out)

        self.assertEqual(
            mod.title_sort(
                set(titles),
                key=undouble_chars
            ),
            output
        )
        self.assertEqual(
            mod.title_sort(
                set(titles),
                key=undouble_chars,
                reverse=True
            ),
            list(reversed(output))
        )

        for i, (title, out) in enumerate(zip(titles, output)):
            titles[i] = {"title": title}
            output[i] = {"title": out}

        self.assertEqual(
            mod.title_sort(
                tuple(titles),
                key=lambda book: undouble_chars(book["title"])
            ),
            output
        )
        self.assertEqual(
            mod.title_sort(
                tuple(titles),
                reverse=True,
                key=lambda book: undouble_chars(book["title"])
            ),
            list(reversed(output))
        )

    def test_title_sort_with_numbers(self):
        titles = (
            "around the world in 80 days",
            "around the world in 79 days"
        )
        self.assertEqual(
            mod.title_sort(titles),
            [
                "around the world in 80 days",
                "around the world in 79 days"
            ]
        )
        self.assertEqual(
            mod.title_sort(titles, smart_numbers=False),
            [
                "around the world in 79 days",
                "around the world in 80 days"
            ]
        )

        titles = (
            "30,000 ON THE HOOF",
            "thirty thousanc on the hoof",
            "ThirtY ThouSANE on The HOOF"
        )
        self.assertEqual(
            mod.title_sort(titles),
            [
                "thirty thousanc on the hoof",
                "30,000 ON THE HOOF",
                "ThirtY ThouSANE on The HOOF"
            ]
        )


if __name__ == "__main__":
    unittest.main()
