"""
Test all the lists and simple functions that the rest of `book_cataloguing`'s
functions use.
"""

import book_cataloguing.contents as mod
import unittest


class ConstantsTest(unittest.TestCase):
    """
    Make sure the lists LOWERCASE_AUTHOR_WORDS, LOWERCASE_TITLE_WORDS,
    MAC_SURNAMES, and AUTHOR_TITLES look right.
    """
    def test_words_in_global_lists(self):
        self.assertTrue("the" in mod.LOWERCASE_AUTHOR_WORDS)
        self.assertTrue("van" in mod.LOWERCASE_AUTHOR_WORDS)
        self.assertTrue("of" in mod.LOWERCASE_AUTHOR_WORDS)
        self.assertTrue("de" in mod.LOWERCASE_AUTHOR_WORDS)
        self.assertTrue("the" in mod.LOWERCASE_TITLE_WORDS)
        self.assertTrue("a" in mod.LOWERCASE_TITLE_WORDS)
        self.assertTrue("when" in mod.LOWERCASE_TITLE_WORDS)
        self.assertTrue("into" in mod.LOWERCASE_TITLE_WORDS)
        self.assertTrue("macdonald" in mod.MAC_SURNAMES)
        self.assertTrue("maclaughlin" in mod.MAC_SURNAMES)
        self.assertTrue("maccormac" in mod.MAC_SURNAMES)
        self.assertTrue("general" in mod.AUTHOR_TITLES)
        self.assertTrue("lord" in mod.AUTHOR_TITLES)
        self.assertTrue("sir" in mod.AUTHOR_TITLES)
        self.assertTrue("bishop" in mod.AUTHOR_TITLES)
        self.assertTrue("mr" in mod.AUTHOR_TITLES)

    def test_words_not_in_global_lists(self):
        self.assertFalse("bob" in mod.LOWERCASE_AUTHOR_WORDS)
        self.assertFalse("when" in mod.LOWERCASE_AUTHOR_WORDS)
        self.assertFalse("great" in mod.LOWERCASE_AUTHOR_WORDS)
        self.assertFalse("brian" in mod.LOWERCASE_AUTHOR_WORDS)
        self.assertFalse("alice" in mod.LOWERCASE_AUTHOR_WORDS)
        self.assertFalse("thee" in mod.LOWERCASE_TITLE_WORDS)
        self.assertFalse("again" in mod.LOWERCASE_TITLE_WORDS)
        self.assertFalse("still" in mod.LOWERCASE_TITLE_WORDS)
        self.assertFalse("above" in mod.LOWERCASE_TITLE_WORDS)
        self.assertFalse("mcdonald" in mod.MAC_SURNAMES)
        self.assertFalse("macaroni" in mod.MAC_SURNAMES)
        self.assertFalse("machine" in mod.MAC_SURNAMES)
        self.assertFalse("upon" in mod.AUTHOR_TITLES)
        self.assertFalse("great" in mod.AUTHOR_TITLES)
        self.assertFalse("bob" in mod.AUTHOR_TITLES)


class StripAccentsTest(unittest.TestCase):
    """Test the function book_cataloguing._strip_accents()"""
    def test_strip_accents(self):
        self.assertEqual(mod._strip_accents("l'\xeele"), "l'ile")
        self.assertEqual(mod._strip_accents("L'\xceLe"), "L'ILe")
        self.assertEqual(mod._strip_accents(" `apple*"), " `apple*")
        self.assertEqual(mod._strip_accents("\xd9dem\xff!"), "Udemy!")


class IsAlnumTest(unittest.TestCase):
    """Test the function book_cataloguing._is_alnum()"""
    def test_letters(self):
        self.assertTrue(mod._is_alnum("a"))
        self.assertTrue(mod._is_alnum("F"))
        self.assertTrue(mod._is_alnum("z"))
        self.assertTrue(mod._is_alnum("9"))
        self.assertTrue(mod._is_alnum("-", True))

    def test_non_letters(self):
        self.assertFalse(mod._is_alnum("-"))
        self.assertFalse(mod._is_alnum(" "))
        self.assertFalse(mod._is_alnum("^"))
        self.assertFalse(mod._is_alnum("("))
        self.assertFalse(mod._is_alnum("."))
        self.assertFalse(mod._is_alnum("\t"))


class CapitalizeFuncTest(unittest.TestCase):
    """Test the function book_cataloguing._capitalize()"""
    def test_capitalize_func(self):
        self.assertEqual(mod._capitalize("woRd"), "Word")
        self.assertEqual(mod._capitalize("mcdonALD"), "McDonald")
        self.assertEqual(mod._capitalize("macdonALD"), "MacDonald")
        self.assertEqual(mod._capitalize("macaroni"), "Macaroni")
        self.assertEqual(mod._capitalize("MCDONALD", False), "Mcdonald")

    def test_capitalize_func_with_apostrophes(self):
        self.assertEqual(mod._capitalize("O'HARA"), "O'Hara")
        self.assertEqual(mod._capitalize("l'\xeele"), "L'\xcele")
        self.assertEqual(mod._capitalize("d'auLAIRE"), "D'Aulaire")
        self.assertEqual(mod._capitalize("dd'aulaire"), "Dd'aulaire")
        self.assertEqual(mod._capitalize("S'S"), "S's")
        self.assertEqual(mod._capitalize("O\u2019haRa"), "O\u2019Hara")


class IsRomanNumeralTest(unittest.TestCase):
    """Test the function book_cataloguing._is_roman_numeral()"""
    def test_roman_numerals(self):
        self.assertTrue(mod._is_roman_numeral("I"))
        self.assertTrue(mod._is_roman_numeral("IV"))
        self.assertTrue(mod._is_roman_numeral("VI"))
        self.assertTrue(mod._is_roman_numeral("XC"))
        self.assertTrue(mod._is_roman_numeral("DCXXI"))
        self.assertTrue(mod._is_roman_numeral("MMCLV"))
        self.assertTrue(mod._is_roman_numeral("i"))
        self.assertTrue(mod._is_roman_numeral("iv"))
        self.assertTrue(mod._is_roman_numeral("vi"))
        self.assertTrue(mod._is_roman_numeral("xC"))
        self.assertTrue(mod._is_roman_numeral("dCXxi"))
        self.assertTrue(mod._is_roman_numeral("MmcLv"))

    def test_non_roman_numerals(self):
        self.assertFalse(mod._is_roman_numeral("j"))
        self.assertFalse(mod._is_roman_numeral("iiiv"))
        self.assertFalse(mod._is_roman_numeral("i i"))
        self.assertFalse(mod._is_roman_numeral("C!"))
        self.assertFalse(mod._is_roman_numeral("i.v"))
        self.assertFalse(mod._is_roman_numeral("MMT"))
        self.assertFalse(mod._is_roman_numeral(";"))


class Num2WordsTest(unittest.TestCase):
    """Test the function book_cataloguing._num2words_without_and()"""
    def test_num2words_without_and(self):
        self.assertEqual(
            mod._num2words_without_and(123),
            "one hundred twenty-three"
        )
        self.assertEqual(
            mod._num2words_without_and(20000),
            "twenty thousand"
        )
        self.assertEqual(
            mod._num2words_without_and(42),
            "forty-two"
        )
        self.assertEqual(
            mod._num2words_without_and(85612),
            "eighty-five thousand, six hundred twelve"
        )


if __name__ == "__main__":
    unittest.main()
