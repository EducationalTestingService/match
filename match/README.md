# More Detailed Documentation

## match_lines()

```python
def match_lines(original_text, things_to_match)
```

**Parameters**

* `original_text`: `str` containing the original text from which `things_to_match` were extracted, which `match` will now use to retrieve the offsets of `things_to_match` from.
* `things_to_match`: `list` where each element can be a `str` or `list` of `str`.  Each element represents a word, phrase, sentence, arbitrary string, etc. whose offsets we wish to find within `original_text`.

If `things_to_match` is a list of tokenized strings, each element of `things_to_match` is expected to be a `list` of tokens.
For example:

```python
[["Hello", ",", "world", "!"], ["That", "was", "the", "first", "sentence", ";", "here", "is", "the", "second", "."]]
```

`things_to_match` could also be:

```python
["cat", "dog", "octopus"]
```

This function will call `match()` on each element of `things_to_match`.

**Return Value**

A `sorted(set())` of `tuple` objects where each `tuple` contains the staring offset, the ending offset, and the text found between them in `original_text`.  Following our first example, the return value could be:

```python
[(0, 13, "Hello, world!"), (15, 63, "That was the first sentence; here is the second.")]
```

## match()

```python
def match(original_text, word_or_token_list_to_match, clean_text=None)
```

**Parameters**

* `original_text`: `str` containing the original text from which `things_to_match` were extracted, which `match` will now use to retrieve the offsets of `things_to_match` from.
* `word_or_token_list_to_match`: Either a single `str` corresponding to a single token we want offsets for, or a `list` of `str` objects corresponding to a tokenized phrase or sentence we want offsets for.
* `clean_text`: If `None` (default), this function will do some preliminary cleaning of `original_text` to better facilitate the matching process (replacing strange quotation marks with ASCII ones, etc.).  This is a one-to-one process; a single character simply becomes a different single character, so as to not throw off the offsets of `word_or_token_list_to_match` within `original_text`.  Without this cleaning process, `word_or_token_to_match` will probably not match against a text with non-ASCII characters in it, especially if those characters are Windows "smart" quotes.

**Return Value**

A `sorted(set())` of `tuple` objects where each `tuple` contains the staring offset, the ending offset, and the text found between them in `original_text`.  For example, say we're looking for all instances of the word `cat`.  The return value might be:

```python
[(4, 7, "cat"), (15, 18, "cat"), (81, 84, "Cat"), (155, 158, "cat"), (217, 220, "cAT")]
```

### How This Function Works

Much of this hinges on the existance of `finditer()` in Python's `regex` module.  We use a list comprehension to generate a `list` of `(m.start(), m.end(), original_text[m.start():m.end()])` tuples for each match `m` returned by `finditer()`.

When where we're interested in all occurrences of a single token, for example "dog", we simply call `regex.finditer(r'\bdog\b', original_text, regex.U | regex.I)`.  When where we're interested in a sentence or phrase like "Dogs make great pets.", things are not so straightforward.

In this case, it is useful to perform some cleanup of `original_text`, as described above.  This is very helpful because typical tokenization normalizes any non-ASCII characters to ASCII equivalents.  We do the same here, being careful not to expand any single character into multiple ones; that will throw off the offsets, since we are not interested in the offsets from `clean_text`, which the user will never see, but in `original_text`, which the user submitted.

Through thorough testing, I determined that the following two strategies are necessary in order to get the offsets for any tokenized string.

**First**, we attempt to reverse tokenization on the string `" ".join(["Dogs", "make", "great", "pets", "."])` and try to find it directly in `original_text` using `finditer()`.  For my test set, this returned the correct match for over 91% of the cases.

For the remaining test cases, a **second** and slightly more time-consuming method is necessary.

1. Use `finditer()` on `"\s*".join(["Dogs", "make", "great", "pets", "."])`.  This works particularly well for essays because many candidates accidentally insert more whitespace characters than necessary, and toksent and expunct do an excellent job of removing the excess spaces.  However, our offsets need to include those spaces.  Should this fail:
2. Use Levenshtein edit distance, as implemented in `nltk.metrics.distance.edit_distance()`.  For each attempt with edit distance, we extract all strings that start with the same token as the one we're looking for ("Dogs" in this example) that have the same number of characters (as "Dogs make great pets."), and return the one with the lowest edit distance to the search string.

We'll try (2) against the original text and our untokenized version from before, and if that fails, we try edit distance again against the original text and `" ".join(["Dogs", "make", "great", "pets", "."])`. Even if the search string is not in the original text, we'll return the offsets of the string with the lowest edit distance within the original text.


## untokenize()

```python
def untokenize(text)
```

Based on https://github.com/commonsense/simplenlp/blob/master/simplenlp/euro.py#L132.

**Parameters**
   
`text`: A single `str` containing the text (usually a sentence output by a sentence-tokenizer) you'd like to untokenize.

**Return Value**

A UTF8-encoded, regular expression-friendly, untokenized version of `text`.