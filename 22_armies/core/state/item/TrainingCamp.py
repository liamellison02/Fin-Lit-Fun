from typing import Dict, Any

from .Item import Item


class TrainingCamp(Item):

    def __eq__(self, other) -> bool:
        if not isinstance(other, TrainingCamp):
            return False
        return super().__eq__(other)

    def __repr__(self) -> str:
        return "Training Camp"

    # Data transfer

    def gatherData(self) -> Dict[str, Any]:
        data = super().gatherData()
        data["type"] = "trainingCamp"
        return data

    def takeData(self, data: Dict[str, Any]):
        super().takeData(data)
