from src.localization import get_location

class Mapping():
    def __init__(self, location) -> None:
        self.location = location
        self.x, self.y, self.yaw = 0.0, 0.0, 0.0

    def update_loop(self):
        self.x, self.y, self.yaw = map(float, self.location.queue.get_nowait().split(","))
        
