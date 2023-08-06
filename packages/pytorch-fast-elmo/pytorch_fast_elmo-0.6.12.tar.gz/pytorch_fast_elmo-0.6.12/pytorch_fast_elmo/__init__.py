# -*- coding: utf-8 -*-
"""Top-level package for pytorch-fast-elmo."""

__author__ = """Hunt Zhan"""
__email__ = 'huntzhan.dev@gmail.com'
__version__ = '0.6.12'

# To avoid `undefined symbol` error.
import torch

# pylint: disable=no-name-in-module
from pytorch_stateful_lstm import StatefulUnidirectionalLstm
# from _pytorch_fast_elmo import ElmoCharacterEncoder, ScalarMix
from _pytorch_fast_elmo import ElmoCharacterEncoder

from pytorch_fast_elmo.utils import (
        batch_to_char_ids,
        load_and_build_vocab2id,
        batch_to_word_ids,
)

from pytorch_fast_elmo.factory import (
        ElmoCharacterEncoderFactory,
        ElmoWordEmbeddingFactory,
        ElmoLstmFactory,
        ElmoVocabProjectionFactory,
)

from pytorch_fast_elmo.model import (
        ScalarMix,
        FastElmoBase,
        FastElmo,
        FastElmoWordEmbedding,
        FastElmoPlainEncoder,
        FastElmoWordEmbeddingPlainEncoder,
        FastElmoForwardVocabDistrib,
        FastElmoBackwardVocabDistrib,
        FastElmoWordEmbeddingForwardVocabDistrib,
        FastElmoWordEmbeddingBackwardVocabDistrib,
)
