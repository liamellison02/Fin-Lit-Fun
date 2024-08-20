from typing import Tuple

from core.constants import Resource, ItemProperty
from core.logic import Logic
from core.state import GameState, IGameStateListener, City
from .FrameComponent import FrameComponent
from ..control import Label
from ...theme.Theme import Theme
from ...tools import formatResourceBalance


class CityFrame(FrameComponent, IGameStateListener):

    def __init__(self, theme: Theme, logic: Logic, city: City):
        super().__init__(theme)
        self.__logic = logic
        self.__city = city

        self.__nameLabel = Label(theme, city.name)
        self.__nameLabel.setTootip("City name")
        self.__nameLabel.moveRelativeTo("topLeft", self, "topLeft")
        self.addComponent(self.__nameLabel)

        self.__citizensLabel = Label(theme)
        self.__workersLabel = Label(theme)
        self.__merchantsLabel = Label(theme)
        self.addComponent(self.__citizensLabel)
        self.addComponent(self.__workersLabel)
        self.addComponent(self.__merchantsLabel)

        self.__foodLabel = Label(theme)
        self.__granaryLabel = Label(theme)
        self.__growthLabel = Label(theme)
        self.addComponent(self.__foodLabel)
        self.addComponent(self.__granaryLabel)
        self.addComponent(self.__growthLabel)

        self.__woodLabel = Label(theme)
        self.__stoneLabel = Label(theme)
        self.__goldLabel = Label(theme)
        self.addComponent(self.__woodLabel)
        self.addComponent(self.__stoneLabel)
        self.addComponent(self.__goldLabel)

        self.__updateValues()

        # Listeners
        self.__logic.state.registerListener(self)

    def dispose(self):
        self.__logic.state.removeListener(self)

    # GameState listener

    def citizenAssigned(self, state: GameState, cityCell: Tuple[int, int], cell: Tuple[int, int]):
        self.__updateValues()

    def citizenUnassigned(self, state: GameState, cityCell: Tuple[int, int], cell: Tuple[int, int]):
        self.__updateValues()

    def turnChanged(self, state: GameState):
        self.__updateValues()

    def resourcesChanged(self, state: GameState):
        self.__updateValues()

    def __updateValues(self):
        city = self.__city
        rules = self.__logic.rules

        self.__citizensLabel.setMessage(f"{city.getCitizenCount()}<citizen>")
        self.__citizensLabel.setTootip(
            "Total number of citizens.<br><br>"
            "There are as many citizens as houses in the city center.<br><br>"
            "Each citizens can be a worker or a merchant.", 200)
        self.__workersLabel.setMessage(f"{city.getWorkerCount()}<worker>")
        self.__workersLabel.setTootip(
            "Total number of workers.<br><br>"
            "Theses citizens work on tiles in the city area.<br><br>"
            "Their production depends on the worked tiles.", 200)
        self.__merchantsLabel.setMessage(f"{city.getMerchantCount()}<merchant>")
        self.__merchantsLabel.setTootip(
            "Total number of merchants.<br><br>"
            "Theses citizens don't work on tiles.<br><br>"
            "They only produce gold.", 200)

        production = rules.computeCityProduction(city)
        balance = production["balance"]

        self.__foodLabel.setMessage(f"{formatResourceBalance(Resource.FOOD, balance)}<food>")
        self.__foodLabel.setTootip(
            "Food production.<br>"
            f'Base:<align x="8">{formatResourceBalance(Resource.FOOD, production["base"])}<food><br>'
            f'Workers:<align x="8">{formatResourceBalance(Resource.FOOD, production["workers"])}<food><br>'
            f'Mills:<align x="8">{formatResourceBalance(Resource.FOOD, production["mills"])}<food><br>'
            f'Bakery:<align x="8">{formatResourceBalance(Resource.FOOD, production["bakery"])}<food><br>'
            f'Eat:<align x="8">{formatResourceBalance(Resource.FOOD, production["upkeep"], negate=True)}<food><br>'
            f'Balance:<align x="8">{formatResourceBalance(Resource.FOOD, production["balance"])}<food><br>'
        )
        granaryFood = city.getProperty(ItemProperty.GRANARY_FOOD, 0)
        granaryFoodMax = rules.getCityGranarySize(city)
        self.__granaryLabel.setMessage(f"{granaryFood}/{granaryFoodMax}<granary>")
        self.__granaryLabel.setTootip(
            "Amount of food in the granary.<br><br>"
            "Excess food production fills the granary.<br><br>"
            "If the granary is full, excess food production is lost.<br><br>"
            "If food production is negative, the missing food is taken from the granary.<br><br>"
            "If there is not enough food to feed everyone, the city loses citizens.", 200
        )
        growthFood = city.getProperty(ItemProperty.GROWTH_POINTS, 0)
        growthFoodMax = rules.getCityGrowthMax(city)
        self.__growthLabel.setMessage(f"{growthFood}/{growthFoodMax}<growth>")
        self.__growthLabel.setTootip(
            "Number of growth points.<br><br>"
            "The city earns a point if everyone is fed.<br><br>"
            f"With {growthFoodMax} point(s), a new citizen appears if there is room for a house in the city center.<br><br>"
            "If there is not enough food, points goes back to zero.", 200
        )
        
        self.__woodLabel.setMessage(f"{formatResourceBalance(Resource.WOOD, balance)}<wood>")
        self.__woodLabel.setTootip(
            "Wood production.<br>"
            f'Base:<align x="8">{formatResourceBalance(Resource.WOOD, production["base"])}<wood><br>'
            f'Workers:<align x="8">{formatResourceBalance(Resource.WOOD, production["workers"])}<wood><br>'
            f'Sawmills:<align x="8">{formatResourceBalance(Resource.WOOD, production["sawmills"])}<wood><br>'
            f'Factory:<align x="8">{formatResourceBalance(Resource.WOOD, production["factory"])}<wood><br>'
            f'Upkeep:<align x="8">{formatResourceBalance(Resource.WOOD, production["upkeep"], negate=True)}<wood><br>'
            f'Balance:<align x="8">{formatResourceBalance(Resource.WOOD, production["balance"])}<wood><br>'
        )
        
        self.__stoneLabel.setMessage(f"{formatResourceBalance(Resource.STONE, balance)}<stone>")
        self.__stoneLabel.setTootip(
            "Stone production.<br>"
            f'Base:<align x="8">{formatResourceBalance(Resource.STONE, production["base"])}<stone><br>'
            f'Workers:<align x="8">{formatResourceBalance(Resource.STONE, production["workers"])}<stone><br>'
            f'Upkeep:<align x="8">{formatResourceBalance(Resource.STONE, production["upkeep"], negate=True)}<stone><br>'
            f'Balance:<align x="8">{formatResourceBalance(Resource.STONE, production["balance"])}<stone><br>'
        )
        
        self.__goldLabel.setMessage(f"{formatResourceBalance(Resource.GOLD, balance)}<gold>")
        self.__goldLabel.setTootip(
            "gold production.<br>"
            f'Base:<align x="10">{formatResourceBalance(Resource.GOLD, production["base"])}<gold><br>'
            f'Workers:<align x="10">{formatResourceBalance(Resource.GOLD, production["workers"])}<gold><br>'
            f'Merchants:<align x="10">{formatResourceBalance(Resource.GOLD, production["merchants"])}<gold><br>'
            f'Markets:<align x="10">{formatResourceBalance(Resource.GOLD, production["markets"])}<gold><br>'
            f'Bank:<align x="10">{formatResourceBalance(Resource.GOLD, production["bank"])}<gold><br>'
            f'Upkeep:<align x="10">{formatResourceBalance(Resource.GOLD, production["upkeep"], negate=True)}<gold><br>'
            f'Balance:<align x="10">{formatResourceBalance(Resource.GOLD, production["balance"])}<gold><br>'
        )

        borderSize = self.theme.framePadding
        self.__citizensLabel.moveRelativeTo("topLeft", self.__nameLabel, "bottomLeft", borderSize=borderSize)
        self.__workersLabel.moveRelativeTo("topLeft", self.__citizensLabel, "topRight", borderSize=borderSize)
        self.__merchantsLabel.moveRelativeTo("topLeft", self.__workersLabel, "topRight", borderSize=borderSize)

        self.__foodLabel.moveRelativeTo("topLeft", self.__citizensLabel, "bottomLeft", borderSize=borderSize)
        self.__granaryLabel.moveRelativeTo("topLeft", self.__foodLabel, "topRight", borderSize=borderSize)
        self.__growthLabel.moveRelativeTo("topLeft", self.__granaryLabel, "topRight", borderSize=borderSize)

        self.__woodLabel.moveRelativeTo("topLeft", self.__foodLabel, "bottomLeft", borderSize=borderSize)
        self.__stoneLabel.moveRelativeTo("topLeft", self.__woodLabel, "topRight", borderSize=borderSize)
        self.__goldLabel.moveRelativeTo("topLeft", self.__stoneLabel, "topRight", borderSize=borderSize)

        self.pack()
