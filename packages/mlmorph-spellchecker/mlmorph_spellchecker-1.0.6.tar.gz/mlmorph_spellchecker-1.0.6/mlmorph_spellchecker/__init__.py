"""
Define a family of algorithms, encapsulate each one, and make them
interchangeable. Strategy lets the algorithm vary independently from
clients that use it.
"""
from __future__ import absolute_import

import abc
import importlib
from .suggestion import Suggestion


def getStategies():
    return ['ChilluNormalization',
            'Ykkuka',
            'NtaCorrection',
            'MpaCorrection',
            'VisualSimilarity',
            'PhoneticSimilarity',
            'GeminateConsonants',
            'ViramaInsertion',
            'VowelElongation',
            'VowelShortening',
            'ChilluToConsonantVirama',
            'ConsonantViramaToChillu',
            ]


def getSuggestions(word, analyser):
    # Order of the items in STRATEGIES is important
    STRATEGIES = getStategies()

    weighted_suggestions = {}
    for class_name in STRATEGIES:
        strategy = getattr(importlib.import_module(
            'mlmorph_spellchecker.strategies'), class_name)()
        candidates = Suggestion(strategy).suggest(word)
        for candidate in candidates:
            if candidate in weighted_suggestions:
                continue
            weighted_analysis = analyser.analyse(candidate, True)
            if len(weighted_analysis) > 0:
                weighted_suggestions[candidate] = weighted_analysis[0][1]

    # Sort by the increasing order of weights
    suggestions = sorted(weighted_suggestions.items(), key=lambda t: t[1])
    if len(suggestions) == 0:
        # No suggestions. Try splitting the word after 3rd letter
        for index in range(3, len(word)-3):
            lWord = word[:index]
            rWord = word[index:]
            lAnalysis = analyser.analyse(lWord, False)
            rAnalysis = analyser.analyse(rWord, False)
            if len(lAnalysis) > 0 and len(rAnalysis) > 0:
                suggestions.append([lWord + ' ' + rWord])
                break
    # Return the words array
    return [suggestion[0] for suggestion in suggestions]


def spellcheck(word, analyser):
    analysis = analyser.analyse(word, False)
    return len(analysis) > 0


__all__ = ['spellcheck', 'getSuggestions']
