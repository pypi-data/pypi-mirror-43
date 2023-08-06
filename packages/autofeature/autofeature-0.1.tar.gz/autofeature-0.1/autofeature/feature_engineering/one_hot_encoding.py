from autofeature.feature_engineering.feature_base import FeatureBase
from autofeature.constants import keys
from autofeature.utils import log_handler

import pandas as pd

logger = log_handler.get_logger(__name__)


class OneHotEncoding(FeatureBase):
    def __init__(self, on_entity = None, on_properties = None, prefix = None, dummy_na = False):
        self._on_entity = on_entity
        self._dummy_na = dummy_na

        if len(on_properties) > 1:
            logger.error("FAIL: one hot encoding cannot be operated on more than one columns")
            return
        else:
            self._on_property = on_properties[0]
            self._table = self._on_entity.table[[keys.PRIMARY_KEY, self._on_property]]

        if prefix:
            self._prefix = prefix
        else:
            self._prefix = self._on_property

    def verify(self):
        pass

    def exec(self):
        try:
            tmp = pd.get_dummies(self._table[self._on_property],
                                 dummy_na = self._dummy_na,
                                 prefix = self._prefix,
                                 # dtype=float
                                 )
            re = pd.concat([self._table[keys.PRIMARY_KEY], tmp], axis = 1)
            return re
        except Exception as err:
            logger.error("FAIL: one hot encoding failed {}".format(repr(err)))
            return None
