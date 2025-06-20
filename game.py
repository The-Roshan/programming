from panda3d.core import Point3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import KeyboardButton, LVector3

class RacingGame(ShowBase):
    def __init__(self):
        super().__init__()

        # Load the environment
        self.track = self.loader.loadModel("models/track")
        self.track.reparentTo(self.render)
        self.track.setScale(1.5, 1.5, 1.5)
        self.track.setPos(0, 0, 0)

        # Load the car model
        self.car = self.loader.loadModel("models/car")
        self.car.reparentTo(self.render)
        self.car.setScale(0.5, 0.5, 0.5)
        self.car.setPos(0, 0, 1)

        # Set up camera
        self.disableMouse()
        self.camera.setPos(0, -20, 10)
        self.camera.lookAt(self.car)

        # Car controls
        self.speed = 0.1
        self.turn_speed = 2.0

        # Input keys
        self.key_map = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }
        self.accept("arrow_left", self.update_key_map, ["left", True])
        self.accept("arrow_left-up", self.update_key_map, ["left", False])
        self.accept("arrow_right", self.update_key_map, ["right", True])
        self.accept("arrow_right-up", self.update_key_map, ["right", False])
        self.accept("arrow_up", self.update_key_map, ["up", True])
        self.accept("arrow_up-up", self.update_key_map, ["up", False])
        self.accept("arrow_down", self.update_key_map, ["down", True])
        self.accept("arrow_down-up", self.update_key_map, ["down", False])

        # Task to update car movement
        self.taskMgr.add(self.update_movement, "UpdateMovementTask")

    def update_key_map(self, key, state):
        self.key_map[key] = state

    def update_movement(self, task):
        dt = globalClock.getDt()

        # Update car position
        if self.key_map["up"]:
            self.car.setY(self.car, self.speed * dt * 100)
        if self.key_map["down"]:
            self.car.setY(self.car, -self.speed * dt * 100)
        if self.key_map["left"]:
            self.car.setH(self.car.getH() + self.turn_speed * dt * 50)
        if self.key_map["right"]:
            self.car.setH(self.car.getH() - self.turn_speed * dt * 50)

        return Task.cont

# Run the game
game = RacingGame()
game.run()
