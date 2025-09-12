"""Test the function book_cataloguing.get_sortable_author()"""

import book_cataloguing as mod
import unittest


class GSAWithCorrectCaseTest(unittest.TestCase):
    def test_gsa(self):
        self.assertEqual(
            mod.get_sortable_author(""), ""
        )
        self.assertEqual(
            mod.get_sortable_author(" ."), ""
        )
        self.assertEqual(
            mod.get_sortable_author("john doe"), "Doe, John"
        )
        self.assertEqual(
            mod.get_sortable_author(" /Douglas#ADAMS. "), "Adams, Douglas"
        )
        self.assertEqual(
            mod.get_sortable_author("thucydides"), "Thucydides"
        )
        self.assertEqual(
            mod.get_sortable_author("Charles' Dickens "), "Dickens, Charles'"
        )

    def test_gsa_with_titles(self):
        self.assertEqual(
            mod.get_sortable_author(" Lieutenant. "), ""
        )
        self.assertEqual(
            mod.get_sortable_author("major general smith "), "Smith"
        )
        self.assertEqual(
            mod.get_sortable_author("President george herbert walker bush"),
            "Bush, George Herbert Walker"
        )
        self.assertEqual(
            mod.get_sortable_author("alfred, lord tennyson"),
            "Tennyson, Alfred"
        )

    def test_gsa_with_suffixes(self):
        self.assertEqual(
            mod.get_sortable_author(" john. doe. jr."),
            "Doe Jr., John"
        )
        self.assertEqual(
            mod.get_sortable_author("john doe sr"),
            "Doe Sr., John"
        )
        self.assertEqual(
            mod.get_sortable_author(" MR. JOHN DOE XIV"), "Doe XIV, John"
        )
        self.assertEqual(
            mod.get_sortable_author("jean le doe iii"), "le Doe III, Jean"
        )
        self.assertEqual(
            mod.get_sortable_author("monsieur jean le doe iii"),
            "le Doe III, Jean"
        )

    def test_gsa_with_lowercase_words(self):
        self.assertEqual(
            mod.get_sortable_author(" Van|Loon!"), "van Loon"
        )
        self.assertEqual(
            mod.get_sortable_author("johannes von der Doe. "),
            "von der Doe, Johannes"
        )
        self.assertEqual(
            mod.get_sortable_author("JOHN MR. VON Doe. "), "von Doe, John"
        )

    def test_gsa_with_apostrophes(self):
        self.assertEqual(
            mod.get_sortable_author("mary`o'hara"),
            "O'Hara, Mary"
        )
        self.assertEqual(
            mod.get_sortable_author("mADELEINE=L'Engle"),
            "L'Engle, Madeleine"
        )
        self.assertEqual(
            mod.get_sortable_author("john do'e"),
            "Do'e, John"
        )

    def test_names_with_hyphens(self):
        self.assertEqual(
            mod.get_sortable_author("LOBELIA SACKVILLE-BAGGINS"),
            "Sackville-Baggins, Lobelia"
        )
        self.assertEqual(
            mod.get_sortable_author("MRS. LOBELIA SACKVILLE-BAGGINS"),
            "Sackville-Baggins, Lobelia"
        )
        self.assertEqual(
            mod.get_sortable_author(" gene>stratton-PORTER!"),
            "Stratton-Porter, Gene"
        )

    def test_names_with_initials(self):
        self.assertEqual(
            mod.get_sortable_author("e B. white."),
            "White, E. B."
        )
        self.assertEqual(
            mod.get_sortable_author("LOUISA m. alcott "),
            "Alcott, Louisa M."
        )

    def test_mc_prefixes(self):
        self.assertEqual(
            mod.get_sortable_author("cormac mccarthy"), "MacCarthy, Cormac"
        )
        self.assertEqual(
            mod.get_sortable_author("george macdonald"), "MacDonald, George"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "cormac mccarthy",
                handle_mc_prefix=False
            ),
            "Maccarthy, Cormac"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "george macdonald",
                handle_mc_prefix=False
            ),
            "Macdonald, George"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "cormac mccarthy",
                correct_case=False
            ),
            "maccarthy, cormac"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "george macdonald",
                correct_case=False
            ),
            "macdonald, george"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "cormac mccarthy",
                handle_mc_prefix=False,
                correct_case=False
            ),
            "maccarthy, cormac"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "george macdonald",
                handle_mc_prefix=False,
                correct_case=False
            ),
            "macdonald, george"
        )


class GSAWithoutCorrectCaseTest(unittest.TestCase):
    def test_gsa(self):
        self.assertEqual(
            mod.get_sortable_author(
                "",
                correct_case=False
            ),
            ""
        )
        self.assertEqual(
            mod.get_sortable_author(
                " .",
                correct_case=False
            ),
            ""
        )
        self.assertEqual(
            mod.get_sortable_author(
                "john doe",
                correct_case=False
            ),
            "doe, john"
        )
        self.assertEqual(
            mod.get_sortable_author(
                " /Douglas#ADAMS. ",
                correct_case=False
            ),
            "adams, douglas"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "thucydides",
                correct_case=False
            ),
            "thucydides"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "Charles Dickens ",
                correct_case=False
            ),
            "dickens, charles"
        )

    def test_gsa_with_titles(self):
        self.assertEqual(
            mod.get_sortable_author(
                " Lieutenant. ",
                correct_case=False
            ),
            ""
        )
        self.assertEqual(
            mod.get_sortable_author(
                "major general smith ",
                correct_case=False
            ),
            "smith"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "President george herbert walker bush",
                correct_case=False
            ),
            "bush, george herbert walker"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "Alfred, Lord Tennyson",
                correct_case=False
            ),
            "tennyson, alfred"
        )

    def test_gsa_with_apostrophes(self):
        self.assertEqual(
            mod.get_sortable_author(
                "mary`o'hara",
                correct_case=False
            ),
            "o'hara, mary"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "mADELEINE=L'Engle",
                correct_case=False
            ),
            "l'engle, madeleine"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "john do'e",
                correct_case=False
            ),
            "do'e, john"
        )

    def test_gsa_with_suffixes(self):
        self.assertEqual(
            mod.get_sortable_author(
                " john. doe. jr.",
                correct_case=False
            ),
            "doe jr., john"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "JOHN DOE SR",
                correct_case=False
            ),
            "doe sr., john"
        )
        self.assertEqual(
            mod.get_sortable_author(
                " MR. JOHN DOE XIV",
                correct_case=False
            ),
            "doe xiv, john"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "jean le doe iii",
                correct_case=False
            ),
            "le doe iii, jean"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "monsieur jean le doe iii",
                correct_case=False
            ),
            "le doe iii, jean"
        )

    def test_gsa_with_lowercase_words(self):
        self.assertEqual(
            mod.get_sortable_author(
                " Van|Loon!",
                correct_case=False
            ),
            "van loon"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "johannes von der Doe. ",
                correct_case=False
            ),
            "von der doe, johannes"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "JOHN MR. VON Doe. ",
                correct_case=False
            ),
            "von doe, john"
        )

    def test_names_with_hyphens(self):
        self.assertEqual(
            mod.get_sortable_author(
                "LOBELIA SACKVILLE-BAGGINS",
                correct_case=False
            ),
            "sackville-baggins, lobelia"
        )
        self.assertEqual(
            mod.get_sortable_author(
                "MRS. LOBELIA SACKVILLE-BAGGINS",
                correct_case=False
            ),
            "sackville-baggins, lobelia"
        )
        self.assertEqual(
            mod.get_sortable_author(
                " gene>stratton-PORTER!",
                correct_case=False
            ),
            "stratton-porter, gene"
        )

    def test_names_with_initials(self):
        self.assertEqual(
            mod.get_sortable_author(
                "e B. white.",
                correct_case=False
            ),
            "white, e. b."
        )
        self.assertEqual(
            mod.get_sortable_author(
                "LOUISA m alcott ",
                correct_case=False
            ),
            "alcott, louisa m."
        )


if __name__ == "__main__":
    unittest.main()
