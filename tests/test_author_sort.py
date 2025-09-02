"""Test the function book_cataloguing.author_sort()"""

import book_cataloguing as mod
import random
import unittest

from test_helpers import double_chars, undouble_chars


class AuthorSortTest(unittest.TestCase):
    def test_author_sort(self):
        authors = "Jane Austen", "charles dickenS"
        self.assertEqual(
            mod.author_sort(authors),
            ["Jane Austen", "charles dickenS"]
        )
        authors = (
            "CORmac mcCARthy",
            "geoffrey+ chaucer",
            ".george (Macdonald* "
        )
        self.assertEqual(
            mod.author_sort(authors),
            [
                "geoffrey+ chaucer",
                "CORmac mcCARthy",
                ".george (Macdonald* "
            ]
        )

    def test_author_sort_with_key_and_reverse(self):
        output = [
            "Joyce Lankester Brisley",
            "Paul Creswick",
            "Saint Alphonsus De Ligouri",
            "Francis De Sales",
            "Marguerite deAngeli",
            "St. Alphonsus Liguori",
            "Patrick O'Brian",
            "Emily G. Ramey",
            "Aleksandr Solzhenitsyn",
            "Harriette Taylor Treadwell",
            "Elizabeth Yates",
        ]
        authors = output.copy()
        for i in range(15):
            random.shuffle(authors)
            self.assertEqual(mod.author_sort(authors), output)
            self.assertEqual(
                mod.author_sort(
                    authors,
                    reverse=True
                ),
                list(reversed(output))
            )

        for i, (author, out) in enumerate(zip(authors, output)):
            authors[i] = double_chars(author)
            output[i] = double_chars(out)

        self.assertEqual(
            mod.author_sort(
                set(authors),
                key=undouble_chars
            ),
            output
        )
        self.assertEqual(
            mod.author_sort(
                set(authors),
                key=undouble_chars,
                reverse=True
            ),
            list(reversed(output))
        )

        for i, (author, out) in enumerate(zip(authors, output)):
            authors[i] = {"author": author}
            output[i] = {"author": out}

        self.assertEqual(
            mod.author_sort(
                tuple(authors),
                key=lambda book: undouble_chars(book["author"])
            ),
            output
        )
        self.assertEqual(
            mod.author_sort(
                tuple(authors),
                reverse=True,
                key=lambda book: undouble_chars(book["author"])
            ),
            list(reversed(output))
        )

    def test_author_sort_with_special_cases(self):
        authors = (
            "richard henry dANa jR.",
            "RICHARD HENRY DANA SR.",
            "riCHArd hENry DANa"
        )
        self.assertEqual(
            mod.author_sort(authors),
            [
                "riCHArd hENry DANa",
                "richard henry dANa jR.",
                "RICHARD HENRY DANA SR."
            ]
        )

        self.assertEqual(
            mod.author_sort((
                "alfred, lord tennyson",
                "alfred, tennysom",
                "Alfred Tennysoo"
            )),
            [
                "alfred, tennysom",
                "alfred, lord tennyson",
                "Alfred Tennysoo"
            ]
        )

        authors = (
            "jean le doe III",
            "jean le doe IIIV",
            "jean le dof",
            "jean lddoe",
            "jean lfdoe"
        )
        self.assertEqual(
            mod.author_sort(authors),
            [
                "jean le doe IIIV",
                "jean lddoe",
                "jean le doe III",
                "jean le dof",
                "jean lfdoe"
            ]
        )

        authors = (
            "gene stratton-porter",
            "gene stratton porter",
            "gene strattop-porter",
            "gene strattol-porter",
            "gend stratton-porter",
            "genf stratton-porter"
        )
        self.assertEqual(
            mod.author_sort(authors),
            [
                "gene stratton porter",
                "gene strattol-porter",
                "gend stratton-porter",
                "gene stratton-porter",
                "genf stratton-porter",
                "gene strattop-porter"
            ]
        )

    def test_sort_one_word_author_names(self):
        authors = (
            "voltaire",
            "monsieur voltaire"
        )
        self.assertEqual(
            mod.author_sort(authors),
            [
                "voltaire",
                "monsieur voltaire"
            ]
        )
        authors = (
            "monsieur voltaire",
            "voltaire"
        )
        self.assertEqual(
            mod.author_sort(authors),
            [
                "monsieur voltaire",
                "voltaire"
            ]
        )
        authors = (
            "geoffrey chaucer",
            "chaucer",
            "dante",
            "dante alighieri"
        )
        self.assertEqual(
            mod.author_sort(authors),
            [
                "dante alighieri",
                "chaucer",
                "geoffrey chaucer",
                "dante"
            ]
        )


if __name__ == "__main__":
    unittest.main()
