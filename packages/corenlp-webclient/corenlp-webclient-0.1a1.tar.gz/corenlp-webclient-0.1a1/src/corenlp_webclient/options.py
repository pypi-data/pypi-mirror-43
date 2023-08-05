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


@dataclass
class WordsToSentenceOptions(BaseOptions):
    """Options of Words-To-Sentence Annotator

    see: https://stanfordnlp.github.io/CoreNLP/ssplit.html
    """
    eolonly: Optional[bool] = None
    isOneSentence: Optional[bool] = None
    newlineIsSentenceBreak: Optional[NewlineIsSentenceBreak] = None
    boundaryMultiTokenRegex: Optional[str] = None
    boundaryTokenRegex: Optional[str] = None
    boundariesToDiscard: Optional[str] = None
    htmlBoundariesToDiscard: Optional[str] = None
    tokenPatternsToDiscard: Optional[str] = None
    boundaryFollowersRegex: Optional[str] = None
