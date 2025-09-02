"""Test the internal function `book_cataloguing.contents._list_of_words()`"""

import book_cataloguing.contents as mod
import unittest


class ListOfWordsTest(unittest.TestCase):
    def test_list_of_words_func(self):
        self.assertEqual(mod._list_of_words(""), ([], 0))
        self.assertEqual(mod._list_of_words("a"), (["a"], 1))
        self.assertEqual(mod._list_of_words("#."), (["#."], 0))
        self.assertEqual(
            mod._list_of_words("three-word string"),
            (["three", "-", "word", " ", "string"], 3)
        )
        self.assertEqual(
            mod._list_of_words("@apple + banana..."),
            (["@", "apple", " + ", "banana", "..."], 2)
        )
        self.assertEqual(
            mod._list_of_words(" This: /sentence-has\tfive5(words?"),
            (
                [
                    " ",
                    "This",
                    ": /",
                    "sentence",
                    "-",
                    "has",
                    "\t",
                    "five5",
                    "(",
                    "words",
                    "?"
                ],
                5
            )
        )

    def test_list_of_words_with_alpha_only(self):
        self.assertEqual(
            mod._list_of_words("@apple + banana...", True),
            (["apple", "banana"], 2)
        )
        self.assertEqual(
            mod._list_of_words(" $two *words`", True),
            (["two", "words"], 2)
        )
        self.assertEqual(
            mod._list_of_words("another three-word string ", True),
            (["another", "three-word", "string"], 3)
        )
        self.assertEqual(
            mod._list_of_words("TEsting  more(hyphen-Joined=Words", True),
            (["TEsting", "more", "hyphen-Joined", "Words"], 4)
        )
        self.assertEqual(
            mod._list_of_words("What - about spaced -out hyphens?", True),
            (["What", "-", "about", "spaced", "-out", "hyphens"], 6)
        )


if __name__ == "__main__":
    unittest.main()
