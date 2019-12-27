match
=====

|Build Status|

|Latest Version|\ |Downloads|

The purpose of the module ``Match`` is to get the offsets (as well as
the string between those offsets, for debugging) of a cleaned-up,
tokenized string from its original, untokenized source. “Big deal,” you
might say, but this is actually a pretty difficult task if the original
text is sufficiently messy, not to mention rife with Unicode characters.

Consider some text, stored in a variable ``original_text``, like:

::

   I   am writing a letter !  Sometimes,I forget to put spaces (and do weird stuff with punctuation)  ?  J'aurai une pomme, s'il vous plâit !

This will/should/might be properly tokenized as:

.. code:: python

   [['I', 'am', 'writing', 'a', 'letter', '!'],
    ['Sometimes', ',', 'I', 'forget', 'to', 'put', 'spaces', '-LRB-', 'and', 'do', 'weird', 'stuff', 'with', 'punctuation', '-RRB-', '?'],
    ["J'aurai", 'une', 'pomme', ',', "s'il", 'vous', 'plâit', '!']]

Now:

.. code:: python

   In [2]: import match

   In [3]: match.match(original_text, ['-LRB-', 'and', 'do', 'weird', 'stuff', 'with', 'punctuation', '-RRB-'])
   Out[3]: [(60, 97, '(and do weird stuff with punctuation)')]

   In [4]: match.match(original_text, ['I', 'am', 'writing', 'a', 'letter', '!'])
   Out[4]: [(0, 25, 'I   am writing a letter !')]

   In [5]: match.match(original_text, ["s'il", 'vous', 'plâit', '!'])
   Out[5]: [(121, 138, "s'il vous plâit !")]

The return type from ``match()`` is a ``list`` because it will return
*all* occurrences of the argument, be it a ``list`` of tokens or a
single ``string`` (word):

.. code:: python

   In [6]: match.match(original_text, "I")
   Out[6]: [(0, 1, 'I'), (37, 38, 'I')]

When passing in a single ``string``, ``match()`` is expecting that
``string`` to be a single word or token. Thus:

.. code:: python

   In [7]: match.match("****because,the****", "because , the")
   Out[7]: []

Try passing in ``"because , the".split(' ')`` instead, or better yet,
the output from a proper tokenizer.

For convenience, a function called ``match_lines()`` is provided:

.. code:: python

   In [8]: match.match_lines(original_text, [ 
      ...: ['-LRB-', 'and', 'do', 'weird', 'stuff', 'with', 'punctuation', '-RRB-'], 
      ...: ['I', 'am', 'writing', 'a', 'letter', '!'], 
      ...: "I" 
      ...: ])
   Out[8]:
   [(0, 1, 'I'),
    (0, 25, 'I   am writing a letter !'),
    (37, 38, 'I'),
    (60, 97, '(and do weird stuff with punctuation)')]

The values returned will always be sorted by their offsets.

Installation
------------

``pip install match``, or for Mac OS X and 64-bit Linux:

::

   $ conda install -c dmnapolitano match

Requirements
------------

-  Python >= 3.4
-  `nltk <http://www.nltk.org>`__
-  `regex <https://pypi.python.org/pypi/regex>`__

Documentation
-------------

`Here! <match>`__.

.. |Build Status| image:: https://travis-ci.org/EducationalTestingService/match.svg?branch=master
   :target: https://travis-ci.org/EducationalTestingService/match
.. |Latest Version| image:: https://img.shields.io/pypi/v/match.svg
   :target: https://pypi.python.org/pypi/match/
.. |Downloads| image:: https://img.shields.io/pypi/dm/match.svg
   :target: https://pypi.python.org/pypi/match/
