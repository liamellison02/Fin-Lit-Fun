from abc import ABC, abstractmethod
from typing import Dict, Any


class IDataTransfer(ABC):

    @abstractmethod
    def gatherData(self) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    def takeData(self, data: Dict[str, Any]):
        raise NotImplementedError()
