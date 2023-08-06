"""
SPOOKIFY
Halloween name generator
<https://github.com/georgewatson/spookify>

George Watson, 2018
Available under an MIT licence
(see LICENSE file, or https://opensource.org/licenses/MIT)

Spookifies all words of 3 or more characters.
To force a match for words shorter than 3 characters, append some dots or
something.

Dependencies:
- Standard:
    json
    os
    random
    regex
    string
    sys     (__main__.py only)
- Third-party:
    jellyfish <https://pypi.org/project/jellyfish/>
        Available through pip (pip install jellyfish)
    pkg_resources

Provides the following functions:
    spookify(name[, list_type][, shuffle])*
        The main function
        Returns a punned-upon version of the string 'name', using the selected
        wordlist; by default, spooky Halloween substitutions are used
    best_substitution(word, possible_subs[, shuffle])*
        Performs the best substitution of a member of possible_subs into word
    score_substitution(word_part, possible_sub)
        Scores the desirability of replacing word_part with possible_sub
(Functions marked * include pseudo-random elements, which may be disabled by
setting shuffle=False if this is undesirable)

For information on how to run spookify interactively, see __main__.py

See README.md for more details.
"""

import json
import os
import random
import string
import pkg_resources
import jellyfish
import regex as re


def best_substitution(word, possible_subs, shuffle=True):
    """
    Finds the best possible substitution in a given word,
    and returns the modified word.
    Longer substitutions are preferred.
    In the case of a tie, a substitution is chosen at random if shuffle=True;
    otherwise, the first substitution wins.

    Arguments (? indicates optional):
        str   word          A word upon which to pun
        [str] possible_subs A list of words that may be inserted into 'word'
    ?   bool  shuffle       Should the lists be shuffled before sorting?
                            Default: True

    Note: The return value of this function may not be fixed if shuffle=True.
    """
    # Skip short words
    if len(word) < 3 or word in ['and', 'for', 'the']:
        return word

    # Get all substrings of length >= 3.
    substrings = [word[i:j+1]
                  for i in range(len(word) - 2)
                  for j in range(i+2, len(word))]

    # Shuffle elements if desired.
    if shuffle:
        substrings = random.sample(substrings, len(substrings))
        substitutions = random.sample(possible_subs, len(possible_subs))
    else:
        substitutions = possible_subs.copy()

    # Find the best spooky substitution.
    # The lists are sorted by length to encourage longer substitutions.
    best_sub = min([(name_part,
                     substitution,
                     score_substitution(name_part, substitution))
                    for name_part in sorted(substrings,
                                            key=len,
                                            reverse=True)
                    for substitution in sorted(substitutions,
                                               key=len,
                                               reverse=True)],
                   key=lambda t: t[2])

    # Substitute the relevant substring,
    # delimited by hyphens,
    # but remove the hyphens at word boundaries.
    return re.sub(r'^-|-$', "", word.replace(best_sub[0], "-"+best_sub[1]+"-"))


def score_substitution(word_part, possible_sub, vowels='aeiouy'):
    """
    Determines the score of a substitution, between 0 and 1 (lower is better)
    Criteria:
        Identical words score 0.
        Substitutions are given a score equal to:
            Half their normalized Damerau-Levenshtein distance
                (the number of insertions, deletions, substitutions &
                transpositions, divided by the length of the substitution),
            plus a penalty of 0.5 points added if the vowels in word_part do
                not form a substring of the vowels in possible_sub.

    Arguments:
        str word_part       Substring to maybe be replaced with 'possible_sub'
        str possible_sub    The string with which 'word_part' may be replaced
    ?   str vowels          Characters to consider as vowels
                            Default: 'aeiouy'
                            Pass a falsey value to disable vowel matching
    """
    # If we care about vowels,
    # get the vowels in each string, in order.
    if vowels:
        word_vowels, sub_vowels = [''.join([c for c in list(letters)
                                            if c in vowels])
                                   for letters in [word_part, possible_sub]]

    # Final score is
    # half the normalised Damerau-Levenshtein distance,
    # plus a half-point penalty if the vowels don't align.
    return (jellyfish.damerau_levenshtein_distance(possible_sub, word_part) /
            ((2 if vowels else 1) * len(possible_sub)) +
            (0.5 if vowels and word_vowels not in sub_vowels else 0))


def spookify(name, list_type='spooky', shuffle=True):
    """
    Spookify
    Generates a spooky version of a provided string, intended for names.
    This acts as the main function for the 'spookify' module.
    See 'spookify' module docstring for more info.

    Arguments (? indicates optional):
        str  name       A name (or other string) on which to pun
    ?   str  list_type  The wordlist to use
                        Default: 'spooky'
                        <list_type>.json must exist in spookify/wordlists
    ?   bool shuffle    Should the lists be shuffled?
                        Default: True

    Note: The return value of this function may not be fixed if shuffle=True.
    This function takes input from a json file stored in the package directory.
    """

    # Import the word list from a JSON-formatted file.
    # If no file with that name exists, default to spooky.
    filename = pkg_resources.resource_filename(
        'spookify',
        os.path.join('wordlists', ''.join([list_type.lower(), '.json'])))
    if not os.path.isfile(filename):
        filename = pkg_resources.resource_filename(
            'spookify',
            os.path.join('wordlists', 'spooky.json'))
    with open(filename, 'r') as word_file:
        word_list = json.load(word_file)

    # Construct a new name
    # by applying the best substitution to each word.
    # Words are sorted by length to encourage longer substitutions.
    return string.capwords(" ".join(
        [best_substitution(name_word, word_list, shuffle=shuffle)
         for name_word in name.lower().split()]))

# eof
