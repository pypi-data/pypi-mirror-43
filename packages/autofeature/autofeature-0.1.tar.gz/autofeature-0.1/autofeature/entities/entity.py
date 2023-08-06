import pandas as pd
import numpy as np

from autofeature.constants import modes
from autofeature.utils import log_handler

logger = log_handler.get_logger(__name__)


class Entity(object):
	"""
	for general entity use
	"""
	def __init__(self, entity_name, data_path, is_root, primary_key, foreign_key = None):
		self._entity_name = entity_name
		self._data_path = data_path
		self._is_root = is_root
		self._primary_key = primary_key
		self._foreign_key = foreign_key

		self._mode = None  # set to get table of train, dev or apply
		self._table = None
		self._train_table = None
		self._dev_table = None
		self._apply_table = None
		
	def initialize(self, is_training = True):

		try:
			self._table = pd.read_csv(self._data_path)
			logger.info("INFO: get table from {} successfully".format(self._data_path))
			if is_training:  # train dev split for training
				if self._is_root:
					self._train_table, self._dev_table = train_dev_split_util(self._table)
					logger.info("INFO: train dev split successfully")
				else:
					logger.info("INFO: no split taken")
			else:
				self._apply_table = self._table  # TODO: how to filter apply data?
				logger.info("INFO: set apply table successfully")
		except Exception as err:
			logger.error("get table from {0} failed {1}".format(self._data_path, repr(err)))

	def set_mode(self, mode):
		if mode == modes.TRAIN:
			if self._train_table is not None:
				self._mode = mode
			else:
				logger.error("FAIL: no train table available for train mode")

		elif mode == modes.DEV:
			if self._dev_table is not None:
				self._mode = mode
			else:
				logger.error("FAIL: no dev table available for dev mode")

		elif mode == modes.APPLY:
			if self._apply_table is not None:
				self._mode = mode
			else:
				logger.error("FAIL: no apply table available for apply mode")

		else:
			logger.error("FAIL: mode not recognized")

	@property
	def mode(self):
		return self._mode

	@property
	def table(self):
		if self._mode == modes.TRAIN:
			return self._train_table
		elif self._mode == modes.DEV:
			return self._dev_table
		elif self._mode == modes.APPLY:
			return self._apply_table
		else:
			return self._table

	@property
	def train_table(self):
		return self._train_table

	@property
	def dev_table(self):
		return self._dev_table

	@property
	def entity_name(self):
		return self._entity_name

	@property
	def data_path(self):
		return self._data_path

	@property
	def is_root(self):
		return self._is_root

	@property
	def foreign_key(self):
		return self._foreign_key

	@property
	def primary_key(self):
		return self._primary_key

	@property
	def key_table(self):
		if self._foreign_key:
			return self.table[[self._primary_key, self._foreign_key]]
		else:
			return self.table[[self._primary_key]]

	# def get_property(self, key):
	# 	if key in self._properties:
	# 		return self._properties[key]
	# 	else:
	# 		return None


def train_dev_split_util(raw_df, rate = 0.5):
	mask = np.random.rand(len(raw_df)) < rate
	train = raw_df[mask]
	dev = raw_df[~mask]
	return train, dev
