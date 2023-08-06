from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd

from bi.models.object import BaseObject


class BaseDataset(BaseObject, ABC):
    """Base abstract class for all datasets.
    """

    @abstractmethod
    def get_dataframe(self, params: Dict = None) -> pd.DataFrame:
        """Returns x and y axes data (maybe several).

        Returns:
            Pandas dataframe.
        """
        pass
