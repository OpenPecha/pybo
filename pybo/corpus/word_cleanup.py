# coding: utf-8
from botok import NAMCHE, TSEK, TokChunks


def word_cleanup(string):
    """If it is Tibetan text, returns the cleaned up syllables, otherwise the original string"""

    def join_syls(syls):
        return "".join([syl if syl.endswith(NAMCHE) else syl + TSEK for syl in syls])

    syls = TokChunks(string).get_syls()
    if syls:
        return join_syls(syls)
    else:
        return string
