"""Test the function book_cataloguing.get_sortable_title()"""

import book_cataloguing as mod
import unittest


class GetSortableTitleWithCorrectCaseTest(unittest.TestCase):
    def test_get_sortable_title(self):
        self.assertEqual(
            mod.get_sortable_title(""),
            ""
        )
        self.assertEqual(
            mod.get_sortable_title("#. "),
            ""
        )
        self.assertEqual(
            mod.get_sortable_title("|a "),
            ""
        )
        self.assertEqual(
            mod.get_sortable_title("|the  *HOB/BIT)"),
            "Hobbit"
        )
        self.assertEqual(
            mod.get_sortable_title(" THE Fell*owship of The --RING"),
            "Fellowship of the Ring"
        )
        self.assertEqual(
            mod.get_sortable_title("an episode of sparrows"),
            "Episode of Sparrows"
        )
        self.assertEqual(
            mod.get_sortable_title("TREASURE ISLAND"),
            "Treasure Island"
        )

    def test_get_sortable_title_with_numbers(self):
        self.assertEqual(
            mod.get_sortable_title(" 20000 leagues UN.DER THE SEA"),
            "Twenty Thousand Leagues Under the Sea"
        )
        self.assertEqual(
            mod.get_sortable_title("@30,000 on+ th]e Hoof :"),
            "Thirty Thousand on the Hoof"
        )
        self.assertEqual(
            mod.get_sortable_title("around the world in 8,0 days"),
            "Around the World in Eighty Days"
        )
        self.assertEqual(
            mod.get_sortable_title(" 2004 leagues UN.DER THE SEA"),
            "Two Thousand Four Leagues Under the Sea"
        )
        self.assertEqual(
            mod.get_sortable_title("the 1st 2 lives of lukas-kasha"),
            "First Two Lives of Lukas-Kasha"
        )
        self.assertEqual(
            mod.get_sortable_title("the 291nd life of lukas-kasha"),
            "Two Hundred Ninety-First Life of Lukas-Kasha"
        )
        self.assertEqual(
            mod.get_sortable_title(
                "@30,000 on+ th]e Hoof :",
                smart_numbers=False
            ),
            "30000 on the Hoof"
        )
        self.assertEqual(
            mod.get_sortable_title(
                "around the world in 8,0 days",
                smart_numbers=False
            ),
            "Around the World in 80 Days"
        )

    def test_mc_prefixes(self):
        self.assertEqual(
            mod.get_sortable_title(
                "a biography of george macdonald",
            ),
            "Biography of George MacDonald"
        )
        self.assertEqual(
            mod.get_sortable_title(
                "A BIOGRAPHY OF GEORGE MACDONALD",
                handle_mc_prefix=False
            ),
            "Biography of George Macdonald"
        )


class GetSortableTitleWithoutCorrectCaseTest(unittest.TestCase):
    def test_get_sortable_title(self):
        self.assertEqual(
            mod.get_sortable_title(
                "",
                correct_case=False
            ),
            ""
        )
        self.assertEqual(
            mod.get_sortable_title(
                "#. ",
                correct_case=False
            ),
            ""
        )
        self.assertEqual(
            mod.get_sortable_title(
                "|a ",
                correct_case=False
            ),
            ""
        )
        self.assertEqual(
            mod.get_sortable_title(
                "|the  *HOB/BIT)",
                correct_case=False
            ),
            "hobbit"
        )
        self.assertEqual(
            mod.get_sortable_title(
                " THE Fell*owship of The --RING",
                correct_case=False
            ),
            "fellowship of the ring"
        )
        self.assertEqual(
            mod.get_sortable_title(
                "an episode of sparrows",
                correct_case=False
            ),
            "episode of sparrows"
        )
        self.assertEqual(
            mod.get_sortable_title(
                "TREASURE ISLAND",
                correct_case=False
            ),
            "treasure island"
        )

    def test_other_cases(self):
        self.assertEqual(
            mod.get_sortable_title(
                "A Biography of George MacDonald",
                correct_case=False
            ),
            "biography of george macdonald"
        )
        self.assertEqual(
            mod.get_sortable_title(
                "A Biography of George MacDonald",
                correct_case=False,
                handle_mc_prefix=False
            ),
            "biography of george macdonald"
        )
        self.assertEqual(
            mod.get_sortable_title(
                "around the world in 80 days",
                correct_case=False
            ),
            "around the world in eighty days"
        )
        self.assertEqual(
            mod.get_sortable_title(
                "the 291nd life of lukas-kasha",
                correct_case=False
            ),
            "two hundred ninety-first life of lukas-kasha"
        )
        self.assertEqual(
            mod.get_sortable_title(
                "around the world in 8,0 days",
                correct_case=False,
                smart_numbers=False
            ),
            "around the world in 80 days"
        )


if __name__ == "__main__":
    unittest.main()
