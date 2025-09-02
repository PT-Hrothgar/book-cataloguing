"""Test the function `book_cataloguing.capitalize_title()`"""

import book_cataloguing as mod
import unittest


class CapitalizeTitleTest(unittest.TestCase):
    def test_capitalize_title_func(self):
        self.assertEqual(mod.capitalize_title("tom sawyer"), "Tom Sawyer")
        self.assertEqual(
            mod.capitalize_title("the adventures of tOM SAWYER"),
            "The Adventures of Tom Sawyer"
        )
        self.assertEqual(
            mod.capitalize_title(
                "cobra iI: the INSide story of The invasion and occupation of "
                "iRAQ"
            ),
            "Cobra II: The Inside Story of the Invasion and Occupation of Iraq"
        )
        self.assertEqual(
            mod.capitalize_title(
                "#.cobra\nii :|thE<>INSide story of~ The!invasion(AND)occupati"
                "on`of iRAQ$$"
            ),
            "#.Cobra\nII :|The<>Inside Story of~ the!Invasion(and)Occupation`o"
            "f Iraq$$"
        )

    def test_capitalize_title_with_mc_prefix(self):
        self.assertEqual(
            mod.capitalize_title(" a biography of george macdonald "),
            " A Biography of George MacDonald "
        )
        self.assertEqual(
            mod.capitalize_title(
                " a biography of george MacDonald ",
                handle_mc_prefix=False
            ),
            " A Biography of George Macdonald "
        )

    def test_capitalize_title_with_hyphens(self):
        self.assertEqual(
            mod.capitalize_title(" a  TItle|ending-with.and "),
            " A  Title|Ending-with.And "
        )
        self.assertEqual(
            mod.capitalize_title("the thirteen-gun salute"),
            "The Thirteen-Gun Salute"
        )
        # A Poe short story that's a little tricky:
        self.assertEqual(
            mod.capitalize_title("X-ING A PARAGRAB"),
            "X-ing a Paragrab"
        )


if __name__ == "__main__":
    unittest.main()
