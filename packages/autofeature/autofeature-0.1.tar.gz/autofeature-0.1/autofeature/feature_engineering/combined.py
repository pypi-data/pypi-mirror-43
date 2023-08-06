from autofeature.feature_engineering.feature_base import FeatureBase
from autofeature.constants import keys, ops
from autofeature.utils import log_handler

import pandas as pd

logger = log_handler.get_logger(__name__)


class Combined(FeatureBase):
    def __init__(self, ops_list: list, name, return_name = "NOT DEFINED"):
        super().__init__(name)
        self._ops_list = ops_list
        if name == ops.TA:
            self._ot, self._oa = ops_list
            self._on_entity = self._ot.on_entity
        elif name == ops.AT:
            self._oa, self._ot = ops_list
            self._on_entity = self._oa.on_entity
        elif name == ops.AAT:
            self._oa1, self._oa2, self._ot = ops_list
            assert self._oa1.on_entity == self._oa2.on_entity
            self._on_entity = self._oa1.on_entity
        else:
            logger.warn("waring: combine name not recognized")
            return
        self._return_name = return_name
        self.__function_dict = {
                            ops.TA: self.__exec_ta,
                            ops.AT: self.__exec_at,
                            ops.AAT: self.__exec_aat,
                            }

    def verify(self):
        pass

    def exec(self):
        re = self.__function_dict[self._name].__call__()
        if re is None:
            logger.error("FAIL: combined ops {0} on entity {1} failed".format(self._name, self._on_entity.entity_name))
            return None
        return re

    def __exec_ta(self):
        try:
            tmp_table = self._ot.exec()
            key_table = self._on_entity.key_table
            tmp_table = pd.merge(tmp_table, key_table, how='inner', on=keys.PRIMARY_KEY).drop([keys.PRIMARY_KEY], axis=1)
            self._oa.set_table(tmp_table)
            self._oa.set_return_name(self._return_name)
            re = self._oa.exec()
            return re
        except Exception as err:
            logger.error("FAIL: combined ops ta failed {}".format(repr(err)))
            return None

    def __exec_at(self):
        try:
            tmp_table = self._oa.exec()
            self._ot.set_join_key(tmp_table[[keys.FOREIGN_KEY]])
            self._ot.set_table(tmp_table.drop([keys.FOREIGN_KEY], axis=1))
            self._ot.set_return_name(self._return_name)
            re = self._ot.exec()
            return re
        except Exception as err:
            logger.error("FAIL: combined ops at failed {}".format(repr(err)))
            return None

    def __exec_aat(self):
        try:
            tmp_table_1 = self._oa1.exec()
            tmp_table_2 = self._oa2.exec()
            tmp_table = pd.merge(tmp_table_1, tmp_table_2, how="outer", on=keys.FOREIGN_KEY)
            self._ot.set_join_key(tmp_table[[keys.FOREIGN_KEY]])
            self._ot.set_table(tmp_table.drop([keys.FOREIGN_KEY], axis=1))
            self._ot.set_return_name(self._return_name)
            re = self._ot.exec()
            return re
        except Exception as err:
            logger.error("FAIL: combined ops aat failed {}".format(repr(err)))
            return None

    @property
    def ops_list(self):
        return self._ops_list
