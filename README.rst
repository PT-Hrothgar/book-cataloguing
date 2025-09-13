Book Cataloguing
================

Correctly capitalize and sort the titles and authors of books.


Basic Usage
-----------

To capitalize the title of a book:

>>> from book_cataloguing import capitalize_title
>>> capitalize_title("the lord of the rings")
'The Lord of the Rings'
>>> capitalize_title("the hobbit: or, there and back again")
'The Hobbit: Or, There and Back Again'


To capitalize the author of a book:

>>> from book_cataloguing import capitalize_author
>>> capitalize_author("HILDA VAN STOCKUM")
'Hilda van Stockum'
>>> capitalize_author("pope john paul ii")
'Pope John Paul II'


To sort some book titles case-insensitively:

>>> from book_cataloguing import title_sort
>>> titles = [
...     "the restaurant at the end of the universe",
...     "so long, and thanks for all the fish",
...     "Mostly Harmless"
... ]
>>> title_sort(titles)
['Mostly Harmless', 'the restaurant at the end of the universe', 'so long, and thanks for all the fish']
>>> title_sort(titles, reverse=True)
['so long, and thanks for all the fish', 'the restaurant at the end of the universe', 'Mostly Harmless']

Please see the online documentation at http://book-cataloguing.readthedocs.io for complete details on these functions and many others.
