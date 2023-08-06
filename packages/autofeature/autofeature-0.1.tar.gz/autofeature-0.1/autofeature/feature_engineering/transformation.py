from autofeature.feature_engineering.feature_base import FeatureBase
from autofeature.feature_engineering.one_hot_encoding import OneHotEncoding
from autofeature.constants import ops, keys
from autofeature.utils import log_handler

from datetime import datetime
import numpy as np

logger = log_handler.get_logger(__name__)


class Transformation(FeatureBase):
	def __init__(self, name, on_entity = None, on_properties = None, return_name = "NOT DEFINED", optionals = {}):
		super().__init__(name)
		self._on_entity = on_entity
		self._on_properties = on_properties
		self._return_name = return_name
		self.__function_dict = {ops.DAYS_DIFF: self.__trans_days_diff,
								ops.HOUR_OF_DAY: self.__trans_hour_of_day,
								ops.DAY_OF_WEEK: self.__trans_day_of_week,
								ops.WEEK_OF_YEAR: self.__trans_week_of_year,
								ops.MONTH_OF_YEAR: self.__trans_month_of_year,
								ops.QUARTER_OF_YEAR: self.__trans_quarter_of_year,
								ops.CONCAT: self.__trans_concat,
								ops.NORM: self.__trans_normalization,
								ops.MIN_MAX: self.__trans_minmax,
								ops.MIN_BETWEEN: self.__trans_min,
								ops.LOG: self.__trans_log,
								ops.ADD: self.__trans_add,
								ops.DIFF: self.__trans_diff,
								ops.MULTI: self.__trans_multiply,
								ops.DIVIDE: self.__trans_divide}
		if self._on_entity and on_properties:
			if optionals.get("query"):
				logger.info("INFO: apply query {}".format(optionals.get("query")))
				table = self._on_entity.table.query(optionals.get("query"))
				self._join_key = table[[keys.PRIMARY_KEY]]
				self._table = table[[keys.FOREIGN_KEY, self._on_property]]

			self._join_key = self._on_entity.table[[keys.PRIMARY_KEY]]
			self._table = self._on_entity.table[self._on_properties]
		else:
			self._table = None
			self._join_key = None

		self._optionals = optionals
		if self._name not in list(self.__function_dict.keys()) + [ops.OHE, ops.BOOL]:
			logger.error("FAIL: Transformation name {} not valid, must be in one of {}".format(self._name, list(self.__function_dict.keys())))

	def exec(self):
		if self._name == ops.OHE:
			prefix = self._optionals.get("prefix", None)
			dummy_na = self._optionals.get("dummy_na", False)
			trans_ohe = OneHotEncoding(self._on_entity, self._on_properties, prefix, dummy_na)
			re = trans_ohe.exec()
		elif self._name == ops.BOOL:
			if not self._optionals.get("true_condition"):
				logger.error("FAIL: Transformation bool missing keywords true_condition in optionals")
				re = []
			else:
				re = self.__trans_bool(true_condition = self._optionals.get("true_condition"))
		else:
			re = self.__function_dict[self._name].__call__()

		if re is None:
			logger.error("FAIL: Transformation {0} on entity {1} failed".format(self._name, self._on_entity.entity_name))
			return None
		return re

	def set_table(self, table):
		self._table = table

	def set_join_key(self, join_key):
		self._join_key = join_key

	def set_return_name(self, return_name):
		self._return_name = return_name

	def __trans_days_diff(self):
		# support datetime value only
		try:
			re = self._join_key
			re[self._return_name] = [days_diff(str2date(x[0]), str2date(x[1])) for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op days_diff failed {}".format(repr(err)))
			return None

	def __trans_hour_of_day(self):
		# support datetime value only
		try:
			re = self._join_key
			re[self._return_name] = [str2date(x[0], "time").hour for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op hour_of_day failed {}".format(repr(err)))
			return None

	def __trans_day_of_week(self):
		# support datetime value only
		try:
			re = self._join_key
			re[self._return_name] = [str2date(x[0]).isoweekday() for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op day_of_week failed {}".format(repr(err)))
			return None

	def __trans_week_of_year(self):
		# support datetime value only
		try:
			re = self._join_key
			re[self._return_name] = [str2date(x[0]).isocalendar()[1] for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op week_of_year failed {}".format(repr(err)))
			return None

	def __trans_month_of_year(self):
		# support datetime value only
		try:
			re = self._join_key
			re[self._return_name] = [str2date(x[0]).month for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op month_of_year failed {}".format(repr(err)))
			return None

	def __trans_quarter_of_year(self):
		# support datetime value only
		try:
			re = self._join_key
			re[self._return_name] = [str2date(x[0]).month // 4 + 1 for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op month_of_year failed {}".format(repr(err)))
			return None

	def __trans_concat(self):
		# support str value
		try:
			re = self._join_key
			re[self._return_name] = ["$".join(x) for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op concat failed {}".format(repr(err)))
			return None

	def __trans_log(self):
		# support numerical value only
		try:
			re = self._join_key
			re[self._return_name] = np.log(self._table.iloc[:,0])
			return re
		except Exception as err:
			logger.error("FAIL: transformation op log failed {}".format(repr(err)))
			return None

	def __trans_normalization(self):
		pass

	def __trans_minmax(self):
		pass

	def __trans_min(self):
		# support numerical value
		try:
			re = self._join_key
			re[self._return_name] = self._table.min(axis = 1)
			return re
		except Exception as err:
			logger.error("FAIL: transformation op min between failed {}".format(repr(err)))
			return None

	def __trans_max(self):
		# support numerical value only
		try:
			re = self._join_key
			re[self._return_name] = self._table.max(axis = 1)
			return re
		except Exception as err:
			logger.error("FAIL: transformation op max between failed {}".format(repr(err)))
			return None

	def __trans_add(self):
		# support numerical value only
		try:
			re = self._join_key
			re[self._return_name] = [x[0] + x[1] for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op add failed {}".format(repr(err)))
			return None

	def __trans_diff(self):
		# support numerical value only
		try:
			re = self._join_key
			re[self._return_name] = [x[0] - x[1] for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op diff failed {}".format(repr(err)))
			return None

	def __trans_multiply(self):
		# support numerical value only
		try:
			re = self._join_key
			re[self._return_name] = [x[0] * x[1] for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op multi failed {}".format(repr(err)))
			return None

	def __trans_divide(self):
		# support numerical value only
		try:
			re = self._join_key
			re[self._return_name] = [x[0] / x[1] for i, x in self._table.iterrows()]
			return re
		except Exception as err:
			logger.error("FAIL: transformation op divide failed {}".format(repr(err)))
			return None

	def __trans_bool(self, true_condition):
		# TODO: more true conditions support needed
		try:
			re = self._join_key
			cmd, val = true_condition
			if cmd == '==':
				re[self._return_name] = [True if str(x[0]) == val else False for i, x in self._table.iterrows()]
			elif cmd == '>':
				re[self._return_name] = [True if str(x[0]) > val else False for i, x in self._table.iterrows()]
			elif cmd == '>=':
				re[self._return_name] = [True if str(x[0]) >= val else False for i, x in self._table.iterrows()]
			elif cmd == '<':
				re[self._return_name] = [True if str(x[0]) < val else False for i, x in self._table.iterrows()]
			elif cmd == '<=':
				re[self._return_name] = [True if str(x[0]) <= val else False for i, x in self._table.iterrows()]
			else:
				logger.error("FAIL: transformation op bool true_condition not valid {}".format(true_condition))
				return re
			return re
		except Exception as err:
			print("FAIL: transformation op bool failed {}".format(repr(err)))
			return None

	@property
	def key_table(self):
		if self.on_entity in self.on_entity.FOREIGN_KEY_key:
			return self.on_entity.table[[keys.PRIMARY_KEY, keys.FOREIGN_KEY]]
		else:
			return self.on_entity.table[[keys.PRIMARY_KEY]]


def str2date(datetime_str, re_type = "date"):
	if type(datetime_str) is not str:
		return datetime.max
	try:
		date_str, time_str = datetime_str.split(" ")
		if re_type == 'date':
			return datetime.strptime(date_str, "%Y-%m-%d")
		if re_type == 'time':
			return datetime.strptime(time_str, "%H:%M:%SZ")
	except Exception as err:
		logger.error("ERROR: string to date {}".format(repr(err)))
		return None


def days_diff(date1, date2):
	if not date1 or not date2:  # TODO?
		return None
	if date2 is datetime.max:
		return None
	return (date2 - date1).days
