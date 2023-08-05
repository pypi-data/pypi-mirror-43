from enum import Enum
from typing import Optional

from dataclasses import dataclass
from dataclasses_jsonschema import JsonSchemaMixin

__all__ = ['BaseOptions', 'NewlineIsSentenceBreak', 'WordsToSentenceOptions']


class BaseOptions(JsonSchemaMixin):
    pass


class NewlineIsSentenceBreak(Enum):
    """Whether to treat newlines as sentence breaks
    """
    ALWAYS = 'always'
    NEVER = 'never'
    TWO = 'two'


@dataclass(order=True, frozen=True)
class WordsToSentenceOptions(BaseOptions):
    """Options of Words-To-Sentence Annotator

    see: https://stanfordnlp.github.io/CoreNLP/ssplit.html
    """
    eolonly: Optional[bool] = None
    is_one_sentence: Optional[bool] = None
    newline_is_sentence_break: Optional[NewlineIsSentenceBreak] = None
    boundary_multi_token_regex: Optional[str] = None
    boundary_token_regex: Optional[str] = None
    boundaries_to_discard: Optional[str] = None
    html_boundaries_to_discard: Optional[str] = None
    token_patterns_to_discard: Optional[str] = None
    boundary_followers_regex: Optional[str] = None
