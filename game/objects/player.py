from game import tag
from enum import Enum


class AssetType(Enum):
    DebitCard = 'DebitCard',
    CheckingAccount = 'CheckingAccount',
    RetirementAccount = 'RetirementAccount',
    Cash = 'Cash',
    Property = 'Property',
    Vehicle = 'Vehicle',
    Miscellaneous = 'Miscellaneous',
    Other = 'Other',
    NoneType = 'NoneType'

    def __str__(self):
        return self.name


class LiabilityType(Enum):
    CreditCardDebt = 'CreditCardDebt',
    StudentLoan = 'StudentLoan',
    VehicleLoan = 'VehicleLoan',
    PersonalLoan = 'PersonalLoan',
    MortgageLoan = 'MortgageLoan',
    Miscellaneous = 'Miscellaneous',
    Other = 'Other',
    NoneType = 'NoneType'

    def __str__(self):
        return self.name


class Asset:
    def __init__(self, asset_type: AssetType, value: float = 0.0, **kwargs):
        self.type = asset_type
        self.value = value
        for key, value in kwargs.items():
            setattr(self, key, value)


class Liability:
    def __init__(self, liability_type: LiabilityType, value: float = 0.0):
        self.type = liability_type
        self.value = value


class StudentLoan(Liability):
    def __init__(self, liability_type: LiabilityType, value: float = 0.0, interest_rate: float = 0.0):
        super().__init__(liability_type, value)
        self.interest_rate = interest_rate

    @tag('OnNewMonth')
    def increment_interest(self):
        self.value += self.value * self.interest_rate
