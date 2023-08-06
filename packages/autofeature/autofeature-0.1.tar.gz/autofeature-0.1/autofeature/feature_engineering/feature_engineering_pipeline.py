from . import Select, Aggregation, Transformation, Combined
from autofeature.constants import modes, keys, paths
from autofeature.entities import *
from autofeature.utils import log_handler

import pandas as pd
import collections, json, os

logger = log_handler.get_logger(__name__)


class FeatureEngineeringPipeline():
	def __init__(self, ops, mode, tenant, version, name):
		self._ops = ops
		self._mode = mode
		self._version = version
		self._name = name
		self._tenant = tenant

		self._train_table = None
		self._dev_table = None
		self._apply_table = None

		self._join = False
		self._unique = True
		self._pipeline = {}

		self._features = []

		if os.getenv(paths.FEP_PATH):
			self._fep_path = os.environ["SAVE_FEP_PATH"]
		else:
			default_path = "/tmp/saved_fep"
			logger.warning("No specified for saved fep, using default {}".format(default_path))
			if not os.path.exists(default_path):
				os.mkdir(default_path)
			self._fep_path = default_path

	def init_pipeline(self):
		"""
		@params;
		@return:

		TODO:

		"""
		for x in self._ops:
			if x.on_entity not in self._pipeline:
				self._pipeline[x.on_entity] = [x]
				if x.on_entity.is_root:
					x.on_entity.set_mode(self._mode)
			else:
				self._pipeline[x.on_entity].append(x)

		if len(self._pipeline.keys()) > 1:
			self._join = True

	def save_pipeline(self, printing = True):
		# save self._pipeline, self._features
		try:
			logger.info("INFO: to serialize pipeline")
			fep = self.serialize_pipeline()
			if printing:
				print(json.dumps(fep, indent=4))
			fname = "{}/fep_{}_{}.json".format(self._fep_path, self._name, self._version)
			with open(fname, "w") as f:
				json.dump(fep, f)
			logger.info("INFO: pipeline saved to {}".format(fname))
			return True
		except Exception as err:
			logger.error("FAIL: saving pipeline job failed {}".format(repr(err)))
			return False

	def load_pipeline(self):
		try:
			logger.info("INFO: to load pipeline")

			fname = "{}/fep_{}_{}.json".format(self._fep_path, self._name, self._version)
			with open(fname, "r") as f:
				fep = json.load(f)
			# print(json.dumps(fep, indent=4))
			self.deserialize_pipeline(fep)
			logger.info("INFO: pipeline loaded successfully")
			return True
		except Exception as err:
			logger.error("FAIL: loading pipeline job failed {}".format(repr(err)))
			return False

	def exec(self):
		"""
		@param:
		@return:
		"""
		outputs = {"ROOT": None, "NODE": []}

		for entity in self._pipeline.keys():
			if not entity.is_root:
				return_table = entity.table[[keys.PRIMARY_KEY, keys.FOREIGN_KEY]]
				outputs["NODE"].append(self.__exec_by_entity(entity, return_table))
			else:
				return_table = entity.table[[keys.PRIMARY_KEY]]
				outputs["ROOT"] = self.__exec_by_entity(entity, return_table)

		if self._join:
			out_table = self.__join_entities(outputs)
		else:
			if outputs["ROOT"]:
				out_table = outputs["ROOT"]
			else:
				out_table = outputs["NODE"][0]  ##TODO: only one node

		if self._mode == modes.TRAIN:
			self._features = list(out_table.columns)
			self._train_table = out_table
			self._train_table.sort_index(axis = 1, inplace = True)
			if keys.TARGET_KEY in self._train_table.columns:
				logger.info("INFO: target feature found, will automatically drop record if target is NA")
				self._train_table = self._train_table.dropna(subset=[keys.TARGET_KEY])
			else:
				logger.warning("WARNING: no target feature is found!")

		if self._mode == modes.DEV or self._mode == modes.APPLY:
			if self._features:
				try:
					curr_features = out_table.columns
					curr_len = len(out_table)
					for fea in self._features:
						if fea not in curr_features:
							out_table[fea] = [0] * curr_len
					if self._mode == modes.DEV:
						self._dev_table = out_table[self._features]
						self._dev_table.sort_index(axis = 1, inplace = True)
						if keys.TARGET_KEY in self._dev_table.columns:
							logger.info("INFO: target feature found, will automatically drop record if target is NA")
							self._dev_table = self._dev_table.dropna(subset=[keys.TARGET_KEY])
						else:
							logger.warning("WARNING: no target feature is found!")
					else:
						self._apply_table = out_table[self._features]
						self._apply_table.sort_index(axis=1, inplace=True)

				except Exception as err:
					logger.error("FAIL: features in dev or apply not consistent with train or saved")

			else:
				logger.error("FAIL: please exec train mode first or load pre-saved pipeline before dev or apply mode")
				return

		logger.info("INFO: pipeline executed successfully!")

	def add_features(self, new_df, join_key, on_train = True, on_dev = True, on_apply = True):
		how = 'inner'  # TODO: what policy for add on features

		try:
			if on_train:
				self._train_table = pd.merge(self._train_table, new_df,
								how=how, left_on=keys.PRIMARY_KEY, right_on=join_key,
								# suffixes=('_ROOT','_NODE'),
								# validate='one_to_many'
									)
			if on_dev:
				self._dev_table = pd.merge(self._dev_table, new_df,
										how=how, left_on=keys.PRIMARY_KEY, right_on=join_key
									)
			if on_apply:
				pass

			logger.info("INFO: new features added and please check tables again")
		except Exception as err:
			logger.info("FAIL: add new features error, {}".format(repr(err)))

	def __join_entities(self, outputs):
		root_table = outputs["ROOT"]
		how = 'left'
		for node_table in outputs["NODE"]:
			if self._unique and keys.PRIMARY_KEY in node_table.columns:
				node_table = node_table.drop([keys.PRIMARY_KEY], axis = 1)

			root_table = pd.merge(root_table, node_table,
								how=how, left_on=keys.PRIMARY_KEY, right_on=keys.FOREIGN_KEY,
								suffixes=('_ROOT','_NODE'),
								# validate='one_to_many'
								)
		if self._unique:
			root_table = root_table.drop_duplicates()
		return root_table

	def __exec_by_entity(self, entity, return_table):
		for o in self._pipeline[entity]:  # iterate all ops in entity
			if type(o) in [Aggregation, Combined]:
				return_table = update_table(return_table, o.exec(), keys.FOREIGN_KEY)
			elif type(o) in [Transformation, Select]:
				return_table = update_table(return_table, o.exec(), keys.PRIMARY_KEY)
			else:
				logger.error("FAIL: op type not recognized: {}".format(type(o)))
				continue
		return return_table

	def set_mode(self, mode):
		# self.__clear()
		logger.info("INFO: setting pipeline mode to {}".format(mode))
		self._mode = mode
		for entity in self._pipeline:
			if entity.is_root:
				entity.set_mode(self._mode)

	def __clear(self):
		self._pipeline = {}
		self._mode = None

	@property
	def feature_list(self):
		return self._features

	@property
	def train_table(self):
		return self._train_table

	@property
	def dev_table(self):
		return self._dev_table

	@property
	def apply_table(self):
		return self._apply_table

	@property
	def pipeline(self):
		return self._pipeline

	def serialize_pipeline(self):
		def serialize_op(op):
			re = dict()
			re["type"] = str(op.__class__)
			if type(op) in (Transformation, Aggregation):
				re["name"] = op.name
				re["on_properties"] = op.on_properties
				re["return_name"] = op.return_name
				re["optionals"] = op.optionals
			elif type(op) in (Combined,):
				re2 = []
				for o in op.ops_list:
					re2.append(serialize_op(o))
				re['ops_list'] = re2
				re["name"] = op.name
				re["return_name"] = op.return_name
			elif type(op) in (Select,):
				re["on_properties"] = op.on_properties
			return re

		fep = collections.OrderedDict()
		fep["version"] = self._version
		fep["name"] = self._name
		if self._tenant:
			fep["tenant"] = self._tenant
		fep["pipeline"] = {}
		for entity in self._pipeline.keys():
			fep["pipeline"][entity.entity_name] = {}
			fep["pipeline"][entity.entity_name]["data_path"] = entity.data_path
			fep["pipeline"][entity.entity_name]["is_root"] = entity.is_root
			fep["pipeline"][entity.entity_name]["primary_key"] = entity.primary_key
			fep["pipeline"][entity.entity_name]["foreign_key"] = entity.foreign_key

			fep["pipeline"][entity.entity_name]["ops"] = []  # TODO: general entity save more entity attributes
			for op in self._pipeline[entity]:
				fep["pipeline"][entity.entity_name]["ops"].append(serialize_op(op))
		fep["feature_names"] = self._features
		return fep

	def deserialize_pipeline(self, fep):
		self._tenant = fep.get("tenant")
		self._version = fep.get("version")
		self._name = fep.get("name")
		ppl = fep.get("pipeline")

		def create_entity(entity_name, data_path, is_root, primary_key, foreign_key):
			if entity_name == "ServiceRequest":
				return ServiceRequestEntity(tenant=self._tenant)
			elif entity_name == "ServiceRequestItem":
				return ServiceRequestItemEntity(tenant=self._tenant)
			elif entity_name == "ServiceRequestHistory":
				return ServiceRequestHistoryEntity(tenant=self._tenant)
			else:
				logger.info("INFO: general entity {} found".format(entity_name))
				return Entity(entity_name, data_path, is_root, primary_key, foreign_key)

		def create_op(input, entity):
			typ = input["type"]

			if typ == str(Aggregation):
				return Aggregation(name = input.get("name"),
									on_entity = entity,
									on_properties = input.get("on_properties"),
									return_name = input.get("return_name"),
									optionals = input.get("optionals")
									)
			elif typ == str(Transformation):
				return Transformation(name = input.get("name"),
									on_entity = entity,
									on_properties = input.get("on_properties"),
									return_name = input.get("return_name"),
									optionals = input.get("optionals")
									)
			elif typ == str(Combined):
				ops_list = []
				for sub_op in input.get("ops_list"):
					ops_list.append(create_op(sub_op, entity))
				return Combined(ops_list, name=input.get("name"), return_name=input.get("return_name"))
			elif typ == str(Select):
				return Select(on_entity = entity, on_properties = input.get("on_properties"))
		for entity_name in ppl:
			data_path = ppl[entity_name]["data_path"]
			is_root = ppl[entity_name]["is_root"]
			primary_key = ppl[entity_name]["primary_key"]
			foreign_key = ppl[entity_name]["foreign_key"]
			e = create_entity(entity_name, data_path, is_root, primary_key, foreign_key)
			e.initialize()  # TODO: get apply dataset
			ops_list = []
			for op_item in ppl[entity_name]["ops"]:
				ops_list.append(create_op(op_item, e))
			self._pipeline[e] = ops_list

		if len(self._pipeline.keys()) > 1:
			self._join = True
		self._features = fep["feature_names"]


# static functions
def update_table(raw_df, new_df, join_key):
	try:
		new_df = pd.merge(raw_df, new_df, how='outer', on=join_key)
		return new_df
	except Exception as err:
		logger.error("FAIL: update table error")
		return raw_df



