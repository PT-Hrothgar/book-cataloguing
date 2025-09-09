.. py:module:: book_cataloguing
.. py:currentmodule:: book_cataloguing

:py:mod:`~book_cataloguing` module reference
============================================

.. note::

   You may notice that with the current layout of the :py:mod:`book_cataloguing` package, all of these functions are actually defined in the file ``contents.py``. However, this layout is subject to change in future versions of the package; please import functions from ``book_cataloguing`` itself rather than ``book_cataloguing.contents``.

Unicode support?
****************

:py:mod:`book_cataloguing` has some support for non-ASCII characters:

>>> from book_cataloguing import capitalize_title
>>> capitalize_title("l'île noire")
"L'Île Noire"

However, this support is experimental, and subject to change: please do not rely on it for much. **The package does not actually support any language other than English**; it probably will not do a good job capitalizing non-English book titles that are more complicated than the one above.

Changing internal lists
***********************

In the module ``book_cataloguing.contents``, four lists of strings are created for later use by the functions defined therein. The names of these lists are subject to change, but currently they are:

 * ``LOWERCASE_TITLE_WORDS``,
 * ``LOWERCASE_AUTHOR_WORDS``,
 * ``MAC_SURNAMES``,
 * and ``AUTHOR_TITLES``.

(More information on each list is available below in the corresponding function.)

Their starting values are (in the developer's opinion) quite suitable for general use, but a function is provided to change each one, if you choose. In each case, the new strings to put in the list must be in an external file, whose name is passed to the function.

.. autofunction:: set_lowercase_title_words
.. autofunction:: set_lowercase_author_words
.. autofunction:: set_mac_surnames
.. autofunction:: set_author_titles


Other Functions
***************

.. autofunction:: capitalize_title
.. autofunction:: capitalize_author
.. autofunction:: get_sortable_title
.. autofunction:: get_sortable_author
.. autofunction:: title_sort
.. autofunction:: author_sort
