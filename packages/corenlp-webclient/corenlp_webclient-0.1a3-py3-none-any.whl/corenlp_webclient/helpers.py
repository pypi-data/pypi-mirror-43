import os
from itertools import chain
from typing import Any, Dict, List, Type

from .annotators import BaseAnnotator

__all__ = ['WORD_SEP', 'chain_words', 'join_chain_words', 'extract_words',
           'join_extract_words', 'create_annotator', 'make_properties']


def chain_words(data: Dict[str, Any]) -> List[str]:
    return [
        token['word']
        for token in chain.from_iterable(
            sent['tokens'] for sent in data['sentences']
        )
    ]


WORD_SEP = ' '


def join_chain_words(data: Dict[str, Any], s: str = WORD_SEP) -> str:
    return s.join(chain_words(data))


def extract_words(data: Dict[str, Any]) -> List[List[str]]:
    result = list()
    for sent in data['sentences']:
        toks = list()
        for token_obj in sent['tokens']:
            toks.append(token_obj['word'])
        result.append(toks)
    return result


def join_extract_words(data: Dict[str, Any], word_sep: str = WORD_SEP, line_sep=os.linesep) -> str:
    result = list()
    for sent in data['sentences']:
        toks = list()
        for token_obj in sent['tokens']:
            toks.append(token_obj['word'])
        result.append(word_sep.join(toks))
    return line_sep.join(result)


def create_annotator(annotator_class: Type[BaseAnnotator], *args, **kwargs) -> BaseAnnotator:
    options = annotator_class.options_class(*args, **kwargs)
    return annotator_class(options)


def make_properties(*annotators: BaseAnnotator) -> Dict[str, Any]:
    properties_dict = {'outputFormat': 'json'}
    for annotator in annotators:
        if 'annotators' not in properties_dict:
            properties_dict['annotators'] = annotator.name
        else:
            properties_dict['annotators'] += f',{annotator.name}'
        properties_dict.update(annotator.options_dict)
    return properties_dict
