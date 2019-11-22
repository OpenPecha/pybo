# coding: utf-8

from .utils.regex_batch_apply import get_regex_pairs, batch_apply_regex
# from .utils.bo_sorted import bo_sorted
from .pipeline.pipes import pybo_prep, pybo_mod, pybo_form
from .corpus.parse_corrected import parse_corrected, generate_data
from botok import *
import pyewts

__version__ = "0.6.16"
