# -*- coding: utf-8 -*-

#   Copyright 2019, Educational Testing Service
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import regex as re

from nltk.metrics.distance import edit_distance


def match_lines(original_text, things_to_match):
    '''See README.md for a description of how to use this function.'''

    matched_lines = []
    unique_things_to_match = (set(things_to_match)
                              if type(things_to_match[0]) is not list
                              else things_to_match)

    without_smart_quotes = _cleanup_text(original_text)

    for thing in unique_things_to_match:
        if len(thing) == 0:
            continue
        matches = match(original_text, thing, clean_text=without_smart_quotes)
        matched_lines += matches

    return sorted(set(matched_lines))


def match(original_text, word_or_token_list_to_match, clean_text=None):
    '''See README.md for a description of how to use this function.'''

    regex_flags = re.U | re.I

    if len(word_or_token_list_to_match) == 0:
        return []

    if not(clean_text):
        clean_text = _cleanup_text(original_text)

    if type(word_or_token_list_to_match) is list:
        to_match = untokenize(" ".join(word_or_token_list_to_match).strip())
        matches = [(m.start(), m.end(), original_text[m.start():m.end()])
                   for m in re.finditer(re.escape(to_match), clean_text, regex_flags)]
        if len(matches) == 0:
            matches = [(m.start(), m.end(), original_text[m.start():m.end()]) for m in
                       re.finditer(r'\s*'.join(re.escape(w) for w in word_or_token_list_to_match),
                                   original_text, regex_flags)]
            if len(matches) == 0:
                edit_distance_match = _match_by_edit_distance(
                    clean_text, re.sub(r'\\s[\*\+]', r' ', to_match))
                matches = [(m.start(), m.end(), original_text[m.start():m.end()])
                           for m in re.finditer(re.escape(edit_distance_match),
                                                clean_text, regex_flags)]
                if len(matches) == 0:
                    edit_distance_match = _match_by_edit_distance(
                        original_text, re.sub(r'\\s[\*\+]', r' ', to_match))
                    matches = [(m.start(), m.end(), original_text[m.start():m.end()])
                               for m in re.finditer(re.escape(edit_distance_match),
                                                    original_text, regex_flags)]
                    if len(matches) == 0:
                        edit_distance_match = _match_by_edit_distance(
                            original_text, " ".join(word_or_token_list_to_match))
                        matches = [(m.start(), m.end(), original_text[m.start():m.end()])
                                   for m in re.finditer(re.escape(edit_distance_match),
                                                        original_text, regex_flags)]
                        if len(matches) == 0:
                            return []
    else:
        matches = [(m.start(), m.end(), original_text[m.start():m.end()])
                   for m in re.finditer(r'\b' + re.escape(word_or_token_list_to_match) + r'\b',
                                        clean_text, regex_flags)]

    return sorted(matches)


def untokenize(text):
    '''See README.md for a description of how to use this function.'''

    text = text.encode('utf8')

    step1 = re.sub(r'([\*\?])', r'\\\\\1', text.decode("utf8"), re.U)

    step2 = step1.replace("`` ", '"\s*').replace(" ''", '"\s*')
    step2 = step2.replace(" -LRB- ", " [\[\(]")
    step2 = re.sub(r' -RRB- ?', r"[\]\)] ", step2)

    step2a = re.sub(r'\.\.\. *', r'[\.…]{1,3}', step2, re.U)

    step3 = re.sub(r' \\*([.,:;?!%]+)([ \'"`\*])', r"\1\2", step2a)
    step4 = re.sub(r' \\*([,:;?!%]+)$', r'\\s*\\' + r"\1", step3)

    step5 = re.sub(r" '", r"'", step4)
    step5 = re.sub(r" n't", r"n't", step5)
    step5 = step5.replace("can not", "cannot")

    step6 = re.sub(r'( *)` ', r"\1'", step5)

    step7 = step6.strip()

    step8 = re.sub(r' \*$', r'', step7)

    step9 = re.sub(r' ([^\\\*\+])', r'\\s+\1', step8)
    step9 = re.sub(r'\\s[\+\*]$', r'', step9)

    return step9


def _cleanup_text(original_text):
    cleaned = original_text.encode("utf8")
    # Borrowed from code by Dan Blanchard;
    # added more weird quotation marks because they weren't matching w/ the Unicode codes
    non_ascii = [
        ('’', "'"),  # ?
        ('“', '"'),  # ?
        ('”', '"'),  # ?
        (' ', ' '),  # mystery space
        ("\n", ' '),  # newlines
        ("\u2018", "'"),  # left single quotation mark
        ("\u2019", "'"),  # right single quotation mark
        ("\u201c", '"'),  # left double quotation mark
        ("\u201d", '"'),  # right double quotation mark
        ("\u2013", "-"),  # en dash
        ("\u00a0", " ")]  # no-break space
    for (unicode_char, ascii_char) in non_ascii:
        try:
            cleaned = cleaned.replace(bytes(unicode_char, "utf-8"), bytes(ascii_char, "utf-8"))
        except Exception as e:
            cleaned = cleaned.replace(unicode_char.encode("utf-8"), ascii_char.encode("utf-8"))
    cleaned = cleaned.decode("utf8")
    return cleaned


def _match_by_edit_distance(full_text, text_to_match):
    text_to_match = text_to_match.replace("-LRB-", "(").replace("-RRB-", ")")
    text_to_match = text_to_match.replace("-LCB-", "{").replace("-RCB-", "}")
    text_to_match = re.sub(r'\[\\\]\\\)\]$', ')', text_to_match)

    try:
        end_point = (text_to_match.index(" ") if " " in text_to_match else len(text_to_match))
        potential_matches = [full_text[m.start():(m.start() + len(text_to_match) + 1)] for m in
                             re.finditer(re.escape(text_to_match[0:end_point]),
                                         full_text, re.U | re.I)]
    except Exception as e:
        import sys

        print(full_text, file=sys.stderr)
        print(file=sys.stderr)
        print(text_to_match, file=sys.stderr)
        sys.exit(1)

    if len(potential_matches) == 0:
        potential_matches = [full_text[m.start():(m.start() + len(text_to_match) + 1)] for m in
                             re.finditer(re.escape(text_to_match[0]), full_text, re.U)]
    if len(potential_matches) == 0:
        text_to_match = text_to_match.replace("(", "[")
        potential_matches = [full_text[m.start():(m.start() + len(text_to_match) + 1)] for m in
                             re.finditer(re.escape(text_to_match[0]), full_text, re.U)]

    potential_matches = [(p[0:p.rindex(text_to_match[-1])+1]
                          if text_to_match[-1] in p and len(p) > len(text_to_match) else p)
                         for p in potential_matches]

    if len(potential_matches) == 0:
        # No idea why this would ever happen, but it does
        return text_to_match

    match_with_lowest_edit_distance = ""
    lowest_edit_distance = -1
    for match in potential_matches:
        e_d = edit_distance(match, text_to_match)
        if lowest_edit_distance == -1 or e_d <= lowest_edit_distance:
            lowest_edit_distance = e_d
            match_with_lowest_edit_distance = match

    result = match_with_lowest_edit_distance.strip()
    if text_to_match[-1] in result:
        while result[-1] != text_to_match[-1]:
            result = result[0:-1]
    elif text_to_match[-1] == '"' and re.search(r'["”\u201d]', result):
        while result[-1] not in ['"', '”', "\u201d"]:
            result = result[0:-1]
    elif text_to_match[-1] not in [']', '}', ')'] and text_to_match[-2:] != "..":
        while result[-1] != text_to_match[-1]:
            result += full_text[full_text.index(result) + len(result)][-1]

    return result
