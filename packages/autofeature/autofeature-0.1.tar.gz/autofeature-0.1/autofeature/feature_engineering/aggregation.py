from autofeature.feature_engineering.feature_base import FeatureBase
from autofeature.constants import keys, ops
from autofeature.utils import log_handler

logger = log_handler.get_logger(__name__)


class Aggregation(FeatureBase):
	def __init__(self, name, on_entity = None, on_properties = None, return_name = "NOT_DEFINED", optionals = {}):
		super().__init__(name)
		self._on_entity = on_entity
		self._on_properties = on_properties
		self._optionals = optionals
		if on_entity and on_properties:
			if len(self._on_properties) > 1:
				logger.warn("WARNING: aggregation property only take one column")

			self._on_property = on_properties[0]  # TODO: ??
			if optionals.get("query"):
				logger.info("INFO: apply query {}".format(optionals.get("query")))
				self._table = self._on_entity.table.query(optionals.get("query"))[[keys.FOREIGN_KEY, self._on_property]]
			else:
				self._table = self._on_entity.table[[keys.FOREIGN_KEY, self._on_property]]
		else:
			self._table = None

		self._return_name = return_name
		self.__function_dict = {ops.SUM: self.__agg_sum,
								ops.COUNT: self.__agg_count,
								ops.MEAN: self.__agg_mean,
								ops.MEDIAN: self.__agg_median,
								ops.STD: self.__agg_std,
								ops.MAX: self.__agg_max,
								ops.MIN: self.__agg_min,
								}
		if self._name not in self.__function_dict.keys():
			logger.error("FAIL: Aggregation name not valid, must be in one of {}".format(list(self.__function_dict.keys())))

	def set_table(self, table):
		self._table = table

	def set_return_name(self, return_name):
		self._return_name = return_name

	def verify(self):
		pass

	def exec(self):
		re = self.__function_dict[self._name].__call__()
		if re is None:
			logger.error("FAIL: aggregation {0} on entity {1} failed".format(self._name, self._on_entity.entity_name))
			return None
		return re

	def __agg_sum(self):
		try:
			re = self._table.groupby([keys.FOREIGN_KEY], as_index=False).sum()
			re.columns = [keys.FOREIGN_KEY, self._return_name]
			return re
		except Exception as err:
			logger.error("FAIL: aggregation op sum failed {}".format(repr(err)))
			return None

	def __agg_mean(self):
		try:
			re = self._table.groupby([keys.FOREIGN_KEY], as_index=False).mean()
			re.columns = [keys.FOREIGN_KEY, self._return_name]
			return re
		except Exception as err:
			logger.error("FAIL: aggregation op mean failed {}".format(repr(err)))
			return None

	def __agg_std(self):
		pass

	def __agg_median(self):
		pass

	def __agg_max(self):
		try:
			re = self._table.groupby([keys.FOREIGN_KEY], as_index=False).max()
			re.columns = [keys.FOREIGN_KEY, self._return_name]
			return re
		except Exception as err:
			logger.error("FAIL: aggregation op max failed {}".format(repr(err)))
			return None

	def __agg_min(self):
		try:
			re = self._table.groupby([keys.FOREIGN_KEY], as_index=False).min()
			re.columns = [keys.FOREIGN_KEY, self._return_name]
			return re
		except Exception as err:
			logger.error("FAIL: aggregation op min failed {}".format(repr(err)))
			return None

	def __agg_count(self):
		try:
			re = self._table.groupby([keys.FOREIGN_KEY], as_index=False).count()
			re.columns = [keys.FOREIGN_KEY, self._return_name]
			return re
		except Exception as err:
			logger.error("FAIL: aggregation op count failed {}".format(repr(err)))
			return None
