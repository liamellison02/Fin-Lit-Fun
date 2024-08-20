from core.constants import Resource
from core.logic import Logic
from core.state import GameState, IGameStateListener
from .FrameComponent import FrameComponent
from ..control import Label
from ...theme.Theme import Theme
from ...tools import formatResourceBalance


class ResourcesFrame(FrameComponent, IGameStateListener):

    def __init__(self, theme: Theme, logic: Logic):
        super().__init__(theme)
        self.__logic = logic

        self.__playerLabel = Label(theme)
        self.addComponent(self.__playerLabel)

        self.__woodLabel = Label(theme, "0<wood>")
        self.addComponent(self.__woodLabel)

        self.__stoneLabel = Label(theme, "0<stone>")
        self.__stoneLabel.setTootip("Current stocks of stone (<stone>), and production per turn")
        self.addComponent(self.__stoneLabel)

        self.__goldLabel = Label(theme, "0<gold>")
        self.__goldLabel.setTootip("Current stocks of gold (<gold>), and production per turn")
        self.addComponent(self.__goldLabel)

        self.__updateValues()

        # Listeners
        self.__logic.state.registerListener(self)

    def dispose(self):
        self.__logic.state.removeListener(self)

    # GameState listener

    def turnChanged(self, state: GameState):
        self.__updateValues()

    def resourcesChanged(self, state: GameState):
        self.__updateValues()

    def __updateValues(self):
        player = self.__logic.state.getPlayer()
        rules = self.__logic.rules
        production = rules.computePlayerProduction(player.id)
        wood = player.getResource(Resource.WOOD)
        woodBalance = formatResourceBalance(Resource.WOOD, production["balance"])
        stone = player.getResource(Resource.STONE)
        stoneBalance = formatResourceBalance(Resource.STONE, production["balance"])
        gold = player.getResource(Resource.GOLD)
        goldBalance = formatResourceBalance(Resource.GOLD, production["balance"])

        maxCityName = 5
        productionBreakdown = {
            Resource.WOOD: "",
            Resource.STONE: "",
            Resource.GOLD: "",
        }
        cities = production["cities"]
        if cities:
            maxCityName = max([len(name) for name in cities.keys()]) + 1
            for cityName in sorted(cities.keys()):
                cityBalance = cities[cityName]["production"]["balance"]
                productionBreakdown[Resource.WOOD] += f'{cityName}:<align x="{maxCityName}"> {formatResourceBalance(Resource.WOOD, cityBalance)}<wood><br>'
                productionBreakdown[Resource.STONE] += f'{cityName}:<align x="{maxCityName}"> {formatResourceBalance(Resource.STONE, cityBalance)}<stone><br>'
                productionBreakdown[Resource.GOLD] += f'{cityName}:<align x="{maxCityName}"> {formatResourceBalance(Resource.GOLD, cityBalance)}<gold><br>'
        else:
            maxCityName = 0

        unitsUpkeep = production["upkeep"]
        productionBreakdown[Resource.WOOD] += f'Upkeep:<align x="{maxCityName}"> {formatResourceBalance(Resource.WOOD, unitsUpkeep)}<wood><br>'
        productionBreakdown[Resource.STONE] += f'Upkeep:<align x="{maxCityName}"> {formatResourceBalance(Resource.STONE, unitsUpkeep)}<stone><br>'
        productionBreakdown[Resource.GOLD] += f'Upkeep:<align x="{maxCityName}"> {formatResourceBalance(Resource.GOLD, unitsUpkeep)}<gold><br>'

        productionBreakdown[Resource.WOOD] += f'Balance:<align x="{maxCityName}"> {woodBalance}<wood>'
        productionBreakdown[Resource.STONE] += f'Balance:<align x="{maxCityName}"> {stoneBalance}<stone>'
        productionBreakdown[Resource.GOLD] += f'Balance:<align x="{maxCityName}"> {goldBalance}<gold>'

        self.__playerLabel.setMessage(f'<flag player="{player.id}">')
        self.__playerLabel.setTootip(f"The current player is {player.name}")

        self.__woodLabel.setMessage(f"{wood: 4}({woodBalance})<wood>")
        self.__woodLabel.setTootip(
            "Available wood<br><br>" + productionBreakdown[Resource.WOOD]
        )

        self.__stoneLabel.setMessage(f"{stone: 4}({stoneBalance})<stone>")
        self.__stoneLabel.setTootip(
            "Available stone<br><br>" + productionBreakdown[Resource.STONE]
        )

        self.__goldLabel.setMessage(f"{gold: 4}({goldBalance})<gold>")
        self.__goldLabel.setTootip(
            "Available gold<br><br>"
            + productionBreakdown[Resource.GOLD]
        )

        borderSize = self.theme.framePadding
        self.__playerLabel.moveRelativeTo("topLeft", self, "topLeft", borderSize=borderSize)
        self.__woodLabel.moveRelativeTo("topLeft", self.__playerLabel, "topRight", borderSize=borderSize)
        self.__stoneLabel.moveRelativeTo("topLeft", self.__woodLabel, "topRight", borderSize=borderSize)
        self.__goldLabel.moveRelativeTo("topLeft", self.__stoneLabel, "topRight", borderSize=borderSize)

        self.pack()



