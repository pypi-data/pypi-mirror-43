from nltk import word_tokenize, pos_tag
from nltk.stem.wordnet import WordNetLemmatizer


class LemmaTokenizer(object):
	def __init__(self):
		self.__lemma = WordNetLemmatizer()

	def __call__(self, articles):
		try:
			tokens_tagged = pos_tag(articles.split())
			return [self.__lemma.lemmatize(w, self.__conv(t)) for w, t in tokens_tagged]
		except Exception as err:
			print(err)
			return ['']
		
	def __conv(self, t):
		# return 'n'
		if t in ["VB", "VBG", "VBN", "VBP", "VBZ", "CD"]:
			return 'v'
		elif t in ["JJ", "JJS", "JJR"]:
			return 'a'
		else:
			return 'n'