import logging

from core.constants import CellValue
from core.logic import Logic
from core.state import World, GameState
from tools.vector import vectorMulI, vectorSubDiv2I
from ui import UserInterface, Theme
from ui.mode import WorldGameMode
from ui.notification import Notification

logging.basicConfig(level=logging.INFO, format='\r%(asctime)s %(filename)s:%(lineno)d: %(message)s')


# Load state
world = World((100, 80))
world.ground.fill(CellValue.GROUND_EARTH)
state = GameState(world)
state.load("level.json")
logic = Logic(state)

# Create a user interface and run it
theme = Theme()
tileSize = theme.getTileset("ground").tileSize
theme.viewSize = vectorMulI((27, 15), tileSize)
userInterface = UserInterface(theme)
theme.init()
#gameMode = EditGameMode(theme, logic)
gameMode = WorldGameMode(theme, logic)
userInterface.setGameMode(gameMode)
worldSize = vectorMulI(state.world.size, tileSize)
view = vectorSubDiv2I(worldSize, theme.viewSize)
gameMode.viewChanged(view)
userInterface.run()
userInterface.quit()
Notification.getManager().checkEmpty()

