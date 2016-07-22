import nltk
import os

from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader.api import CategorizedCorpusReader
from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader


DOC_PATTERN = r'(?!\.)[\w_\s]+/[\w\s\d\-]+\.txt'
CAT_PATTERN = r'([\w_\s]+)/.*'


class RedBlueCorpusReader(CategorizedPlaintextCorpusReader):

	def __init__(self, root, **kwargs):
		CategorizedPlaintextCorpusReader.__init__(
			self, root, DOC_PATTERN, cat_pattern=CAT_PATTERN
		)


corpus = RedBlueCorpusReader(ROOT)




