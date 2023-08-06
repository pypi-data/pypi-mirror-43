from autofeature.feature_engineering.feature_base import FeatureBase
from autofeature.feature_engineering.tokenizer import LemmaTokenizer
from autofeature.feature_engineering.word2vec import Word2Vector
from autofeature.constants import keys, ops
from autofeature.utils import log_handler

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer

logger = log_handler.get_logger(__name__)


class TextVectorization(FeatureBase):
	def __init__(self, name, on_entity = None, on_properties = None, return_name = None, optionals = {}):
		super().__init__(name)
		self._on_entity = on_entity
		self._on_properties = on_properties
		self._optionals = optionals
		type = optionals["type"]

		if type == "tfidf":
			max_df = optionals.get("max_df") or 0.95
			min_df = optionals.get("min_df") or 0.0
			max_features = optionals.get("max_features") or 3000
			lang = optionals.get("language") or "en"
			ngram_min = optionals.get("ngram_min") or 1
			ngram_max = optionals.get("ngram_max") or 1
			self.__vectorizer = TfidfVectorizer(max_df=max_df,
												min_df=min_df,
												max_features=max_features,
												tokenizer=LemmaTokenizer(),
												ngram_range=(ngram_min, ngram_max),
												stop_words=lang,
												lowercase=True,
												# token_pattern = '[a-zA-Z\-][a-zA-Z\-]{2,}'
												)
		elif type == "word2vec":
			self.__vectorizer = Word2Vector()

	def verify(self):
		pass

	def exec(self):
		pass
