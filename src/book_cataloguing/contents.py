# Python >=3.9
from pathlib import Path as _Path
from re import search as _search
from string import ascii_letters as _ascii_letters, digits as _digits
from typing import Any, Callable, Iterator, Optional, Union

import unicodedata as _unicodedata

from num2words import num2words as _num2words
import roman_numerals as _rn

_MODULE_DIR = _Path(__file__).resolve().parent


def _filename_to_list(
    filename: str,
    prepend_module_dir: bool = True
) -> list[str]:
    if prepend_module_dir:
        filename = str(_MODULE_DIR / filename)

    with open(filename) as file:
        return file.read().strip().lower().splitlines()


APOSTROPHES = "'\x91\x92\u2018\u2019"

# We will populate these four lists in a moment...
LOWERCASE_TITLE_WORDS = []
LOWERCASE_AUTHOR_WORDS = []
MAC_SURNAMES = []
AUTHOR_TITLES = []
# ...using these four functions:


def set_lowercase_title_words(filename: Optional[str] = None) -> None:
    """
    Get a new list of lowercase words in book titles from a file.

    In the file should be words like "the", "a", and "of", that should not
    be capitalized when they are in the title of a book (unless they are at
    the beginning or end of a title or subtitle.)

    The referenced file should have one word on each line. The case of the
    words does not matter, and they need not be sorted in any particular
    order.

    If ``filename`` is None, the default file for this list
    (``book_cataloguing/lowercase_title_words.txt``) will be used.
    """
    LOWERCASE_TITLE_WORDS.clear()

    if filename is None:
        args = "lowercase_title_words.txt", True
    else:
        args = filename, False

    LOWERCASE_TITLE_WORDS.extend(_filename_to_list(*args))


def set_lowercase_author_words(filename: Optional[str] = None) -> None:
    """
    Get a new list of lowercase words in author names from a file.

    In the file should be words like "le", "von", and "of", that should not
    be capitalized when they are part of an author's name, and that might be
    part of a multi-word surname (such as "von Neumann").

    The referenced file should have one word on each line. The case of the
    words does not matter, and they need not be sorted in any particular
    order.

    If ``filename`` is None, the default file for this list
    (``book_cataloguing/lowercase_author_words.txt``) will be used.
    """
    LOWERCASE_AUTHOR_WORDS.clear()

    if filename is None:
        args = "lowercase_author_words.txt", True
    else:
        args = filename, False

    LOWERCASE_AUTHOR_WORDS.extend(_filename_to_list(*args))


def set_mac_surnames(filename: Optional[str] = None) -> None:
    """
    Get a new list of surnames starting with "Mac" from a file.

    In the file should be names like "MacDonald", where the fourth letter
    (the letter following the "Mac") should be capitalized.

    The referenced file should have one word on each line. The case of the
    words does not matter, and they need not be sorted in any particular
    order.

    If ``filename`` is None, the default file for this list
    (``book_cataloguing/mac_surnames.txt``) will be used.
    """
    MAC_SURNAMES.clear()

    if filename is None:
        args = "mac_surnames.txt", True
    else:
        args = filename, False

    MAC_SURNAMES.extend(_filename_to_list(*args))


def set_author_titles(filename: Optional[str] = None) -> None:
    """
    Get a new list of author titles from a file.

    In the file should be words like "lord", "mrs", and "president", that,
    when they appear in an author's name, are likely titles rather than part
    of the name itself.

    The referenced file should have one word on each line. The case of the
    words does not matter, and they need not be sorted in any particular
    order.

    If ``filename`` is None, the default file for this list
    (``book_cataloguing/author_titles.txt``) will be used.
    """
    AUTHOR_TITLES.clear()

    if filename is None:
        args = "author_titles.txt", True
    else:
        args = filename, False

    AUTHOR_TITLES.extend(_filename_to_list(*args))


set_lowercase_title_words()
set_lowercase_author_words()
set_mac_surnames()
set_author_titles()


def _(obj: Any) -> Any:
    return obj


def _num2words_without_and(num: int) -> str:
    """
    Internal wrapper for num2words().

    This function converts the given number to words with no "and".
    E.g., 123 becomes "one hundred twenty-three" rather than "one hundred
    and twenty-three."
    """
    return _num2words(num).replace("and ", "")


def _strip_accents(string: str) -> str:
    nfkd_form = _unicodedata.normalize("NFKD", string)
    return "".join([c for c in nfkd_form if not _unicodedata.combining(c)])


def _is_alnum(
    string: Union[str, None],
    include_hyphens: bool = False
) -> "bool | None":
    """
    Internal function for determining whether a character is alphanumeric.

    Return True if the given string is alphanumeric or an apostrophe. It is
    assumed to be one character long.
    Also return True if the string is a hyphen and include_hyphens is True.
    """
    if string is None:
        return None

    string = _strip_accents(string)

    return (
        string in _ascii_letters
        or string in _digits
        or string in APOSTROPHES
        or include_hyphens and string == "-"
    )


def _capitalize(string: str, handle_mc_prefix: bool = True) -> str:
    """
    Internal function for capitalizing a string.

    Handle names like O'Hara correctly, and if handle_mc_prefix is True,
    handle names like MacDonald correctly as well.
    """
    string = string.lower()
    divide = 0

    # Determine if the string is a name like McCarthy where the first and
    # third letters should be capitalized, or MacDonald where the first and
    # fourth letters should be capitalized.
    if handle_mc_prefix:
        if string.startswith("mc"):
            divide = 2
        elif string.startswith("mac"):
            if string in MAC_SURNAMES:
                divide = 3

    # Determine if the string starts with a letter, an apostrophe, and at
    # least two more letters
    if _search(f"^[a-z][{APOSTROPHES}][a-z]{{2,}}", _strip_accents(string)):
        # If so, it is probably a name like "O'Hara" where both the first and
        # third letters should be capitalized.
        divide = 2

    return "".join((
        string[:divide].capitalize(),
        string[divide:].capitalize()
    ))


def _is_roman_numeral(string: str) -> bool:
    """Internal case-insensitive function for finding valid Roman numerals."""
    try:
        _rn.RomanNumeral.from_string(string.lower())
    except _rn.InvalidRomanNumeralError:
        return False
    else:
        return True


def _list_of_words(string: str, alpha_only: bool = False) -> tuple[list, int]:
    """
    Internal function for splitting up strings.

    This function separates a string into a list of alphanumeric and
    non-alphanumeric sections. It returns a 2-tuple where the first element is
    such a list and the second element is the number of alphanumeric sections
    in it.

    E.g.:
    >>> _list_of_words("@apple + banana. ")
    (['@', 'apple', ' + ', 'banana', '. '], 2)
    >>> _list_of_words("//A.four-word (string. ")
    (['//', 'A', '.', 'four', '-', 'word', ' (', 'string', '. '], 4)

    When alpha_only is True, the list will only contain the alphanumeric
    sections, but in this case hyphens will be considered alphanumeric.

    E.g.:
    >>> _list_of_words("//A.three-word (string. ", alpha_only=True)
    (['A', 'three-word', 'string'], 3)
    """
    if not string:
        return [], 0

    # Initialize variables
    result = []
    this_section = []
    word_count = 0
    # Whether or not the section we are on is alphanumeric
    # (we will change this to a boolean value)
    on_word = None
    # Get list of all the characters in the string, plus None to
    # terminate it
    string = list(string) + [None]

    for char in string:
        # Determine if this character belongs in a new section
        if (this_is_alnum := _is_alnum(
            char,
            include_hyphens=alpha_only
        )) != on_word:
            # We will start on a new section of the given string
            # Record the section just created
            new_section = "".join(this_section)

            # We should not append new_section to result if it is empty
            # (The very first section created will be empty, since the on_word
            #  flag starts out as None.)
            if new_section:
                # We should also not append new_section to result if it is
                # non-alphanumeric, AND alpha_only is set to True
                if _is_alnum(
                    new_section[0],
                    include_hyphens=alpha_only
                ) or not alpha_only:
                    result.append(new_section)

            # Initialize new section with its first character
            this_section = [char]
            on_word = this_is_alnum

            if this_is_alnum:
                word_count += 1

        else:
            # This character is part of the previous section
            this_section.append(char)

    return result, word_count


def capitalize_title(title: str, handle_mc_prefix: bool = True) -> str:
    """
    Capitalize a book title, preserving all non-alphanumeric characters.

    This function considers all non-alphanumeric characters except
    apostrophes to separate words, and it converts all words recognized as
    Roman numerals to uppercase. It also capitalizes the second *letter* of
    words starting with any letter followed by an apostrophe (e.g. O'Brien).
    See :ref:`capitalize-title-examples` below.

    :param str title: Title to capitalize.
    :param bool handle_mc_prefix: Whether or not to treat words starting with
        "mc" or "mac" differently. When True, capitalize the third letter of
        all words starting with "mc" (e.g. convert "mcdonald" to "McDonald"),
        and fourth letter of all words starting with "mac" if they are in the
        list of Mac surnames. (You can change this list with the function
        :py:func:`~book_cataloguing.set_mac_surnames`.) When False, capitalize
        only the first letter of such names.
    :returns: Capitalized version of title.
    :rtype: str

    .. _capitalize-title-examples:

    Examples
    --------
    >>> capitalize_title("the hobbit: or, there and back again")
    'The Hobbit: Or, There and Back Again'
    >>> capitalize_title(" THE*LORD =of tHE RIngs]")
    ' The*Lord =of the Rings]'
    >>> capitalize_title("the thirteen-gun salute")
    'The Thirteen-Gun Salute'
    >>> capitalize_title("a midsummer night's dream")
    "A Midsummer Night's Dream"

    Handling of Roman numerals:

    >>> capitalize_title("henry vi, part ii")
    'Henry VI, Part II'

    Handling of name prefixes:

    >>> capitalize_title("A BIOGRAPHY OF GEORGE MACDONALD")
    'A Biography of George MacDonald'
    >>> capitalize_title("a biography of george macdonald", False)
    'A Biography of George Macdonald'
    >>> capitalize_title("a biography of patrick o'brien")
    "A Biography of Patrick O'Brien"
    """
    # Separate title into alphanumeric and non-alphanumeric sections
    sections, total_word_count = _list_of_words(title)
    total_section_count = len(sections)
    # Initialize variables
    word_count = 0
    first = True

    for i, section in enumerate(sections):
        # Don't spend time capitalizing this section if it is non-alphanumeric
        if _is_alnum(section[0]):
            # Assume the corrected version of the word will be all lowercase
            new_section = section.lower()

            # Determine whether or not this is the last word before a colon
            last = False
            if i < total_section_count - 1:
                last = ":" in sections[i + 1]

            # Roman numerals should be all uppercase
            if _is_roman_numeral(section):
                new_section = section.upper()

            elif (
                # Is this the first word of a title or subtitle?
                first
                # Is this a word that should always be capitalized?
                # (That is, is it NOT a word like a/an/and/the that should
                #  sometimes be lowercase?)
                or section.lower() not in LOWERCASE_TITLE_WORDS
                # Is this the last word of the title?
                or word_count == total_word_count - 1
                # Is this the last word before a colon?
                or last
            ):
                # In any of those cases, capitalize word
                new_section = _capitalize(section, handle_mc_prefix)

            # Record corrected version of word
            sections[i] = new_section

            word_count += 1
            # If this is the last word before a colon, "first" should be True
            # for the next word, since it will be the first word of a subtitle
            first = last

    return "".join(sections)


def capitalize_author(author: str, handle_mc_prefix: bool = True) -> str:
    """
    Capitalize the name of an author, preserving non-alphanumeric characters.

    This function considers all non-alphanumeric characters except
    apostrophes to separate words, and it converts all words recognized as
    Roman numerals to uppercase. It also capitalizes the second *letter* of
    words starting with any letter followed by an apostrophe (e.g. O'Brien).
    See :ref:`capitalize-author-examples` below.

    :param str author: Author name to capitalize.
    :param bool handle_mc_prefix: Whether or not to treat words starting with
        "mc" or "mac" differently. When True, capitalize the third letter of
        all words starting with "mc" (e.g. convert "mcdonald" to "McDonald"),
        and fourth letter of all words starting with "mac" if they are in the
        list of Mac surnames. (You can change this list with the function
        :py:func:`~book_cataloguing.set_mac_surnames`.) When False, capitalize
        only the first letter of such names.
    :returns: Capitalized version of author name.
    :rtype: str

    .. _capitalize-author-examples:

    Examples
    --------
    >>> capitalize_author("ludwig van beethoven")
    'Ludwig van Beethoven'
    >>> capitalize_author(" .LEO*TOLstoY =")
    ' .Leo*Tolstoy ='

    Handling of Roman numerals:

    >>> capitalize_author("pope john xxiii")
    'Pope John XXIII'

    Handling of name prefixes:

    >>> capitalize_author("CORMAC MCCARTHY")
    'Cormac McCarthy'
    >>> capitalize_author("cormac mccarthy", False)
    'Cormac Mccarthy'
    >>> capitalize_author("patrick.o'brien")
    "Patrick.O'Brien"
    """
    # Separate author's name into alphanumeric and non-alphanumeric sections
    sections, total_word_count = _list_of_words(author)

    for i, section in enumerate(sections):
        # Don't spend time capitalizing this section if it is non-alphanumeric
        if _is_alnum(section[0]):
            # Assume the correct version of this word will have the first
            # character(s) capitalized with all the rest lowercase
            new_section = _capitalize(section, handle_mc_prefix)

            # Roman numerals should be all uppercase
            if _is_roman_numeral(section):
                new_section = section.upper()

            # If this is a word such as "van" or "of", it should be lowercase
            # (e.g. Ludwig van Beethoven)
            elif section.lower() in LOWERCASE_AUTHOR_WORDS:
                new_section = section.lower()

            # Record correctly capitalized word
            sections[i] = new_section

    return "".join(sections)


def get_sortable_title(
    title: str,
    handle_mc_prefix: bool = True,
    correct_case: bool = True,
    smart_numbers: bool = True,
) -> str:
    title = title.lower()

    # Ensure there are alphanumeric characters in the title
    if not _search("[a-z0-9]", title):
        return ""

    if smart_numbers:
        # Get rid of commas within numbers
        while match := _search(r"\d,\d", title):
            title = "".join((
                title[:match.start() + 1],
                title[match.end() - 1:]
            ))

        # Convert words to numbers
        while match := _search(r"\d+", title):
            title = "".join((
                title[:match.start()],
                _num2words_without_and(match.group()),
                title[match.end():]
            ))

    # Get list of all the words in the title
    sections, section_count = _list_of_words(title)

    # If the title started or ended with spaces or punctuation, remove it
    for i in (0, -1):
        if not _is_alnum(sections[i][0]):
            sections.pop(i)

    # Now the first section is the first word of the title.
    # Remove it if it is "a", "an", or "the"
    if sections[0] in ("a", "an", "the"):
        sections.pop(0)

        # Now the first section is probably the space after "a", "an", or "the"
        # Attempt to remove it
        try:
            sections.pop(0)
        except IndexError:
            # If there was no such section, then "a", "an", or "the" was the
            # only word in the title. In this case, return an empty string
            return ""

    # Replace each non-alphanumeric section
    for i, section in enumerate(sections):
        if not _is_alnum(section[0]):
            # Replace this section with a space if it contains one, otherwise
            # an empty string
            sections[i] = " " if " " in section else ""

    # Construct new title
    new_title = "".join(sections)

    # Correct case of new title, if necessary
    if correct_case:
        new_title = capitalize_title(
            new_title,
            handle_mc_prefix=handle_mc_prefix
        )

    return new_title


def _separate_author_name(
    author: str,
    handle_mc_prefix: bool = True,
    correct_case: bool = True
) -> tuple[str, str]:
    # Get list of only the alphanumeric portions of given author name
    # (These may include hyphens)
    sections, section_count = _list_of_words(author.lower(), True)
    # Remove all words that are titles (e.g. mr, lord, madam)
    sections = list(filter(lambda word: word not in AUTHOR_TITLES, sections))

    # If there are no words left in the author's name, return empty string
    if not sections:
        return ""

    if sections[-1] in ("jr", "sr"):
        # If name ends with "jr" or "sr", add period to the suffix
        sections[-1] = f"{sections[-1]}."
        # The author's last name is in this case two words long instead of one
        divide = -2

    elif _is_roman_numeral(sections[-1]):
        # If name ends with a Roman numeral, the last name is also two words
        # long
        divide = -2
    else:
        # Normally, the last name is only one word
        divide = -1

    # Loop through all words in the name
    for i, section in enumerate(sections):
        # If word is only one word long, it is an initial (unless we're
        # capitalizing Truman's name, but we can't be perfect). Add a period
        # to the end of it.
        if not section[1:]:
            section = f"{section}."

        # Names starting with "mc" should be sorted as if they begin with "mac"
        elif section.startswith("mc"):
            section = f"mac{section[2:]}"

        # Capitalize this word, if "correct_case" is True
        if correct_case:
            section = capitalize_author(
                section,
                handle_mc_prefix=handle_mc_prefix
            )

        # Remove apostrophes from names like O'Hara
        sections[i] = section.replace("'", "")

    # Loop through words just before the last name we found
    for word in sections[divide - 1::-1]:
        # All words such as "de" and "von" should be made part of the last name
        if word in LOWERCASE_AUTHOR_WORDS:
            divide -= 1
        else:
            break

    # Construct entire last name
    last_name = " ".join(sections[divide:])

    # If that leaves no words to be part of the first name, return a
    # 1-element tuple with just the last name
    if not sections[:divide]:
        return (last_name,)

    # Return a tuple containing the last name and then the first name
    return (
        last_name,
        " ".join(sections[:divide])
    )


# XXX doc todo
def get_sortable_author(
    author: str,
    handle_mc_prefix: bool = True,
    correct_case: bool = True
) -> str:
    return ", ".join(_separate_author_name(
        author,
        handle_mc_prefix=handle_mc_prefix,
        correct_case=correct_case
    ))


def _internal_sort(
    iterable: Iterator[Any],
    /,
    process_func: Callable[[str], str],
    *,
    key: Optional[Callable[[Any], str]] = None,
    reverse: bool = False,
    flags: dict[str, bool] = {}
):
    key = key or _

    return sorted(
        iterable,
        key=lambda x: process_func(key(x), **flags),
        reverse=reverse
    )


# XXX doc todo
def title_sort(
    iterable: Iterator[Any],
    /,
    *,
    key: Optional[Callable[[Any], str]] = None,
    reverse: bool = False,
    smart_numbers: bool = True,
) -> list[Any]:
    return _internal_sort(
        iterable,
        get_sortable_title,
        key=key,
        reverse=reverse,
        flags={
            "correct_case": False,
            "smart_numbers": smart_numbers,
        }
    )


# XXX doc todo
def author_sort(
    iterable: Iterator[Any],
    /,
    *,
    key: Optional[Callable[[Any], str]] = None,
    reverse: bool = False,
) -> list[Any]:
    return _internal_sort(
        iterable,
        _separate_author_name,
        key=key,
        reverse=reverse,
        flags={
            "correct_case": False,
        }
    )
