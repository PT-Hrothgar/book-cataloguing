"""Test the function book_cataloguing.capitalize_author()"""

import book_cataloguing as mod
import unittest


class CapitalizeAuthorTest(unittest.TestCase):
    def test_capitalize_author_func(self):
        self.assertEqual(
            mod.capitalize_author("ludwig van beethoven"),
            "Ludwig van Beethoven"
        )
        self.assertEqual(
            mod.capitalize_author("CHARLES DICKENS"),
            "Charles Dickens"
        )
        self.assertEqual(
            mod.capitalize_author(" ~john?von^,neumann )"),
            " ~John?von^,Neumann )"
        )
        self.assertEqual(
            mod.capitalize_author("alexander The great"),
            "Alexander the Great"
        )

    def test_capitalize_authors_with_suffixes(self):
        self.assertEqual(
            mod.capitalize_author("  HENRY#viiI/"),
            "  Henry#VIII/"
        )
        self.assertEqual(
            mod.capitalize_author(" Pope JOHN xxiii "),
            " Pope John XXIII "
        )
        self.assertEqual(
            mod.capitalize_author("john Doe SR. "),
            "John Doe Sr. "
        )

    def test_capitalize_authors_with_prefixes(self):
        self.assertEqual(
            mod.capitalize_author("Patrick `o'brieN. "),
            "Patrick `O'Brien. "
        )
        self.assertEqual(
            mod.capitalize_author("george macdonald"),
            "George MacDonald"
        )
        self.assertEqual(
            mod.capitalize_author("george macdonald", False),
            "George Macdonald"
        )
        self.assertEqual(
            mod.capitalize_author("CORMAC MCCARTHY"),
            "Cormac McCarthy"
        )
        self.assertEqual(
            mod.capitalize_author("CORMAC MCCARTHY", False),
            "Cormac Mccarthy"
        )


if __name__ == "__main__":
    unittest.main()
