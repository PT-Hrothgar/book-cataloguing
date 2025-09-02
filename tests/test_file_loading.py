"""Test the file loading functions in book_cataloguing"""

import book_cataloguing as mod
import os
import unittest


def write(content, filename):
    with open(filename, "w") as file:
        file.write(content)


class FileLoadingTest(unittest.TestCase):
    def test_set_lowercase_title_words(self):
        write("""a
an
the
""", "tmp.txt")
        self.assertEqual(
            mod.capitalize_title("the fellowship of the ring"),
            "The Fellowship of the Ring"
        )
        mod.set_lowercase_title_words("tmp.txt")
        self.assertEqual(
            mod.capitalize_title("the fellowship of the ring"),
            "The Fellowship Of the Ring"
        )
        self.assertEqual(
            mod.capitalize_title("a room with a view"),
            "A Room With a View"
        )
        self.assertEqual(
            mod.capitalize_title("diARY OF aN early american boy"),
            "Diary Of an Early American Boy"
        )
        mod.set_lowercase_title_words()
        self.assertEqual(
            mod.capitalize_title("the fellowship of the ring"),
            "The Fellowship of the Ring"
        )
        os.remove("tmp.txt")

    def test_set_lowercase_author_words(self):
        write("""le
la
the
""", "tmp.txt")
        self.assertEqual(
            mod.capitalize_author("gertrud von le fort"),
            "Gertrud von le Fort"
        )
        self.assertEqual(
            mod.get_sortable_author("gertrud von le fort"),
            "von le Fort, Gertrud"
        )
        mod.set_lowercase_author_words("tmp.txt")
        self.assertEqual(
            mod.capitalize_author("gertrud von le fort"),
            "Gertrud Von le Fort"
        )
        self.assertEqual(
            mod.get_sortable_author("gertrud von le fort"),
            "le Fort, Gertrud Von"
        )
        self.assertEqual(
            mod.get_sortable_author("AlexANDER The greaT"),
            "the Great, Alexander"
        )
        self.assertEqual(
            mod.capitalize_author("LUDWIG VAN beethoven"),
            "Ludwig Van Beethoven"
        )
        mod.set_lowercase_author_words()
        self.assertEqual(
            mod.capitalize_author("gertrud von le fort"),
            "Gertrud von le Fort"
        )
        self.assertEqual(
            mod.get_sortable_author("gertrud von le fort"),
            "von le Fort, Gertrud"
        )
        os.remove("tmp.txt")

    def test_set_mac_surnames(self):
        write("""maCDONald
MAclauGHLIN
""", "tmp.txt")
        self.assertEqual(
            mod.capitalize_author("Somebody named maccormac"),
            "Somebody Named MacCormac"
        )
        mod.set_mac_surnames("tmp.txt")
        self.assertEqual(
            mod.capitalize_author("Somebody named maccormac"),
            "Somebody Named Maccormac"
        )
        self.assertEqual(
            mod.capitalize_author("Somebody named macdonald"),
            "Somebody Named MacDonald"
        )
        self.assertEqual(
            mod.get_sortable_author("a PERSON with the namE oF MACDONalD"),
            "of MacDonald, A. Person With the Name"
        )
        mod.set_mac_surnames()
        self.assertEqual(
            mod.capitalize_author("Somebody named maccormac"),
            "Somebody Named MacCormac"
        )
        os.remove("tmp.txt")

    def test_set_author_titles(self):
        write("""MR
mrs
proFESSOR
""", "tmp.txt")
        self.assertEqual(
            mod.get_sortable_author("alfred, lord tennyson"),
            "Tennyson, Alfred"
        )
        mod.set_author_titles("tmp.txt")
        self.assertEqual(
            mod.get_sortable_author("alfred, lord tennyson"),
            "Tennyson, Alfred Lord"
        )
        self.assertEqual(
            mod.get_sortable_author("mrs. professor SMITH"),
            "Smith"
        )
        self.assertEqual(
            mod.get_sortable_author("mr. admiral SMITH"),
            "Smith, Admiral"
        )
        mod.set_author_titles()
        self.assertEqual(
            mod.get_sortable_author("alfred, lord tennyson"),
            "Tennyson, Alfred"
        )
        self.assertEqual(
            mod.get_sortable_author("mr. admiral SMITH"),
            "Smith"
        )
        os.remove("tmp.txt")


if __name__ == "__main__":
    unittest.main()
