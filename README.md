match
=====

The purpose of the module `Match` is to get the offsets (as well as the string between those offsets, for debugging) of a cleaned-up, tokenized string from its original, untokenized source.  "Big deal," you might say, but this is actually a pretty difficult task if the original text is sufficiently messy, not to mention rife with Unicode characters.

Consider some text, stored in a variable `original_text`, like:

```
I   am writing a letter !  Sometimes,I forget to put spaces (and do weird stuff with punctuation)  ?  J'aurai une pomme, s'il vous plâit !
```

This will/should/might be properly tokenized as:

```python
[[u'I', u'am', u'writing', u'a', u'letter', u'!'],
 [u'Sometimes', u',', u'I', u'forget', u'to', u'put', u'spaces', u'-LRB-', u'and', u'do', u'weird', u'stuff', u'with', u'punctuation', u'-RRB-', u'?'],
 [u"J'aurai", u'une', u'pomme', u',', u"s'il", u'vous', u'pl\xe2it', u'!']]
```

Now:

```python
In [22]: Match.match(original_text, [u'-LRB-', u'and', u'do', u'weird', u'stuff', u'with', u'punctuation', u'-RRB-'])
Out[22]: [(60, 97, u'(and do weird stuff with punctuation)')]

In [23]: Match.match(original_text, [u'I', u'am', u'writing', u'a', u'letter', u'!'])
Out[23]: [(0, 25, u'I   am writing a letter !')]

In [24]: Match.match(original_text, [u"s'il", u'vous', u'pl\xe2it', u'!'])
Out[24]: [(121, 138, u"s'il vous pl\xe2it !")]
```

The return type from `match()` is a `list` because it will return *all* occurrences of the argument, be it a `list` of tokens or a single `string` (word):

```python
In [25]: Match.match(original_text, "I")
Out[25]: [(0, 1, u'I'), (37, 38, u'I')]
```

For convenience, a function called `match_lines()` is provided:
```python
In [26]: Match.match_lines(original_text, [[u'-LRB-', u'and', u'do', u'weird', u'stuff', u'with', u'punctuation', u'-RRB-'], [u'I', u'am', u'writing', u'a', u'letter', u'!'], "I"])
Out[26]: 
[(0, 1, u'I'),
 (0, 25, u'I   am writing a letter !'),
 (37, 38, u'I'),
 (60, 97, u'(and do weird stuff with punctuation)')]
```

The values returned will always be sorted by their offsets.

## Requirements

* Python >= 2.7 (works with both 2.7 and 3.3!)
* [nltk](http://www.nltk.org)
* [regex](https://pypi.python.org/pypi/regex)

## Documentation

Viewable [here](https://rawgithub.com/dmnapolitano/match/master/doc/_build/html/index.html).