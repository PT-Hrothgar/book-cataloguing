# book-cataloguing package
# Correctly capitalize and sort the titles and authors of books.
# Online documentation is at http://book-cataloguing.readthedocs.io.

from book_cataloguing.contents import (
    set_lowercase_title_words,
    set_lowercase_author_words,
    set_mac_surnames,
    set_author_titles,
    capitalize_title,
    capitalize_author,
    get_sortable_title,
    get_sortable_author,
    title_sort,
    author_sort
)


__all__ = [
    "set_lowercase_title_words",
    "set_lowercase_author_words",
    "set_mac_surnames",
    "set_author_titles",
    "capitalize_title",
    "capitalize_author",
    "get_sortable_title",
    "get_sortable_author",
    "title_sort",
    "author_sort"
]
__version__ = "1.0"
