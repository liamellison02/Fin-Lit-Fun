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
        self.value = self.value + (self.value*self.interest_rate)

class NetWorth:
    def __init__(self):
        self.assets = []
        self.liabilities = []

    def add_asset(self, asset: Asset):
        self.assets.append(asset)

    def add_liability(self, liability: Liability):
        self.liabilities.append(liability)

    def calculate_net_worth(self):
        return sum([asset.value for asset in self.assets]) - sum([liability.value for liability in self.liabilities])

    def __str__(self):
        return f'Assets: {self.assets}, Liabilities: {self.liabilities}, Net Worth: {self.calculate_net_worth()}'
    
    
class Player:
    def __init__(self,
                age: int = 16, 
                health: int = 100, 
                happiness: int = 100,
                **kwargs):
        self.age = age
        self.health = health
        self.happiness = happiness
        self.net_worth = NetWorth()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def start_education(self, education):
        self.education = education
        new_loan = StudentLoan("Undergrad Loan", 40000.0, 2.5)
        self.net_worth.liabilities.append(new_loan)

player = Player(name='')