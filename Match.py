# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import regex as re

from nltk.metrics.distance import edit_distance


def match_lines(original_text, things_to_match):
    '''
    :param original_text: ``str``/``Unicode`` containing the original text to get offsets within
    :param things_to_match: ``list(words/phrases)`` whose offsets we wish to find within ``original_text``.

    If ``things_to_match`` is a list of tokenized strings, each element of ``things_to_match`` is expected to be a ``list`` of tokens.
    For example::

        [["Hello", ",", "world", "!"], ["That", "was", "the", "first", "sentence", ";", "here", "is", "the", "second", "."]]

    ``things_to_match`` could also be::

        ["cat", "dog", "octopus"]

    or even a mix of the two.  This function will call :mod:`sourcerater.util.Match.match()` on each element of ``things_to_match``.

    :returns: ``sorted(set([(start, end, word/phrase) for word/phrase in things_to_match]))`` for ALL occurrences of each word/phrase in ``things_to_match``.
    '''
    matched_lines = []
    unique_things_to_match = (set(things_to_match) if type(things_to_match[0]) is not list else things_to_match)
    
    without_smart_quotes = _cleanup_text(original_text)

    for thing in unique_things_to_match:
        if len(thing) == 0:
            continue
        matches = match(original_text, thing, clean_text=without_smart_quotes)
        #if type(matches) is not list:
        #    print(matches)
        #elif len(matches) == 0:
        #    print(thing)
        #else:
        matched_lines += matches

    return sorted(set(matched_lines))


def match(original_text, word_or_token_list_to_match, clean_text=None):
    '''
    :param original_text: ``str``/``Unicode`` containing the original text to get offsets within
    :param word_or_token_list_to_match: Either a single ``str``/``Unicode`` corresponding to a single token we want offsets for, or a ``list(str)`` corresponding to a phrase/sentence we want offsets for.
    :param clean_text: If ``None``, this function will do some preliminary cleaning of ``original_text`` to better facilitate the matching process (replacing strange quotation marks with ASCII ones, etc.).  This is a one-to-one process; a single character simply becomes a different single character, so as to not throw off the offsets of ``word_or_token_list_to_match`` within ``original_text``.  It's just that ``word_or_token_to_match`` will probably not match against a text with non-ASCII characters in it, especially if those characters are Windows "smart" quotes.

    :returns: ``sorted([(start, end, word/phrase)])`` where each ``tuple`` contains a unique occurrence of ``word_or_token_list_to_match`` in ``original_text``, and the word/phrase is what is contained within ``original_text`` at that ``start``/``end`` offset pair.

    **How This Works**

    Much of this hinges on the existance of ``finditer()`` in Python's ``regex`` module.  We use a list 
    comprehension to generate a ``list`` of ``(m.start(), m.end(), original_text[m.start():m.end()])``
    tuples for each match ``m`` returned by ``finditer()``.

    When where we're interested in all occurrences of a single token, for example "dog", we
    simply call ``regex.finditer(r'\bdog\b', original_text, regex.U | regex.I)``.  When where 
    we're interested in a sentence or phrase like "Dogs make great pets.", things are not so 
    straightforward.

    In this case, it is useful to perform some cleanup of ``original_text``, as described above.  This is very
    helpful because tokenization normalizes any non-ASCII characters to ASCII equivalents.  We do the same here,
    being careful not to expand any single character into multiple ones; that will throw off the offsets, since
    we are not interested in the offsets from ``clean_text``, which the user will never see, but in ``original_text``,
    which the user submitted.

    This sentence/phrase matching was tested on a set of 200 randomly-selected essays from GRE and TOEFL (200
    each) from 2011-2012 with complete disregard to score.  Each essay was sentence- and word-tokenized, and
    each word-tokenized sentence was passed to this function along with its essay.  From this, I determined
    that the following two strategies are necessary in order to get the offsets for any tokenized string.

    **First**, we simply reverse tokenization on the string ``" ".join(["Dogs", "make", "great", "pets", "."])``
    and try to find it directly in ``original_text`` using ``finditer()``.  For the test set described
    above, 94.3% of the sentences from the GRE essays and 91.9% of the sentences from the TOEFL essays
    returned the correct match and offsets within the original essay using just this strategy alone.

    For the remaining 6.7% and 9.1% of sentences, respectively, a **second** and more time-consuming
    method is necessary.

    1. Use ``finditer()`` on ``"\s*".join(["Dogs", "make", "great", "pets", "."])``.  This works particularly well for essays because many candidates accidentally insert more whitespace characters than necessary, and toksent and expunct do an excellent job of removing the excess spaces.  However, our offsets need to include those spaces.  Should this fail:
    2. Use Levenshtein edit distance, as implemented in ``nltk.metrics.distance.edit_distance()``.  For each attempt with edit distance, we extract all strings that start with the same token as the one we're looking for ("Dogs" in this example) that have the same number of characters (as "Dogs make great pets."), and return the one with the lowest edit distance to the search string.


    We'll try (2) against the original text and our untokenized version from before, and if that fails, 
    we try edit distance again against the original text and ``" ".join(["Dogs", "make", "great", "pets", "."])``.
    Even if the search string is not in the original text, we'll return the offsets of the string
    with the lowest edit distance within the original text.
    '''

    if len(word_or_token_list_to_match) == 0:
        return []

    if not(clean_text):
        clean_text = _cleanup_text(original_text)

    if type(word_or_token_list_to_match) is list:
        to_match = untokenize(" ".join(word_or_token_list_to_match).strip())
        matches = [(m.start(), m.end(), original_text[m.start():m.end()]) for m in re.finditer(to_match, clean_text, re.U)]
        if len(matches) == 0:
            matches = [(m.start(), m.end(), original_text[m.start():m.end()]) 
                       for m in re.finditer("\s*".join(word_or_token_list_to_match), original_text, re.U)]
            if len(matches) == 0:
                edit_distance_match = _match_by_edit_distance(original_text, to_match)
                matches = [(m.start(), m.end(), original_text[m.start():m.end()]) 
                           for m in re.finditer(re.escape(edit_distance_match), original_text, re.U)]
                if len(matches) == 0:
                    edit_distance_match = _match_by_edit_distance(original_text, " ".join(word_or_token_list_to_match))
                    matches = [(m.start(), m.end(), original_text[m.start():m.end()]) 
                               for m in re.finditer(re.escape(edit_distance_match), original_text, re.U)]
                    if len(matches) == 0:
                        return edit_distance_match
    else:
        matches = [(m.start(), m.end(), original_text[m.start():m.end()]) for m in re.finditer(r'\b' + word_or_token_list_to_match + r'\b', clean_text, re.U | re.I)]

    return sorted(matches)


def untokenize(text):
    '''
    Based on https://github.com/commonsense/simplenlp/blob/master/simplenlp/euro.py#L132
    
    :param text: A single ``str``/``Unicode`` containing the sentence (well, might work on any arbitrary text) you'd like to untokenize.
    :returns: A UTF8-encoded, regular expression-friendly, untokenized version of ``text``.

    .. seealso:: https://github.com/EducationalTestingService/stanford-thrift/blob/master/README_tokenizer.md which isn't actually used here (much slower than this approach)
    '''
    text = text.encode('utf8')

    step1 = text.replace("`` ", '" *').replace(" ''", '" *')
    step2 = step1.replace(" -LRB- ", " [\[\(]")
    step2 = re.sub(r' -RRB- ?', r"[\]\)] ", step2)

    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`\*])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r' *\\' + r"\1", step3)

    step5 = re.sub(r" '", r"'", step4)
    step5 = re.sub(r" n't", r"n't", step5)
    step5 = step5.replace("can not", "cannot")

    step6 = re.sub(r'( *)` ', r"\1'", step5)

    step7 = re.sub(r'\.\.\. *', r'[\.…]{1,3}', step6, re.U)
    step7 = step7.strip()

    step8 = re.sub(r' \*$', r'', step7)

    return step8.decode("utf8")


def _cleanup_text(original_text):
    cleaned = original_text.encode("utf8")
    # Borrowed from toksent; added more weird quotation marks because they weren't matching w/ the Unicode codes
    non_ascii = [
        ('’', "'"), # ?
        ('“', '"'), # ?
        ('”', '"'), # ?
        (' ', ' '), # mystery space
        ("\n", ' '), # newlines
        ("\u2018", "'"), # left single quotation mark
        ("\u2019", "'"), # right single quotation mark
        ("\u201c", '"'), # left double quotation mark
        ("\u201d", '"'), # right double quotation mark
        ("\u2013", "-"), # en dash
        ("\u00a0", " ")] # no-break space
    for (unicode_char, ascii_char) in non_ascii:
        cleaned = cleaned.replace(unicode_char, ascii_char)
    cleaned = cleaned.decode("utf8")
    return cleaned


def _match_by_edit_distance(original_text, text_to_match):
    potential_matches = [original_text[m.start():m.start()+len(text_to_match)] for m in 
                         re.finditer(text_to_match[0:text_to_match.index(" ")], original_text, re.U)]

    if len(potential_matches) == 0:
        # No idea why this would ever happen, but it does
        return text_to_match

    match_with_lowest_edit_distance = ""
    lowest_edit_distance = -1
    for match in potential_matches:
        e_d = edit_distance(match, text_to_match)
        if lowest_edit_distance == -1 or e_d < lowest_edit_distance:
            lowest_edit_distance = e_d
            match_with_lowest_edit_distance = match

    result = match_with_lowest_edit_distance.strip()
    if text_to_match[-1] in result:
        return result[0:result.rindex(text_to_match[-1])+1]
    return result