from app import kernel
from pokemongo_bot.navigation.destination import Destination
from pokemongo_bot.navigation.navigator import Navigator


@kernel.container.register('waypoint_navigator', ['@config.core', '@api_wrapper'])
class WaypointNavigator(Navigator):
    def __init__(self, config, api_wrapper):
        # type: (Namespace, PoGoApi) -> None
        super(WaypointNavigator, self).__init__(config, api_wrapper)

        self.waypoints = config['movement']['navigator_waypoints']
        self.pointer = 0

    def navigate(self, map_cells):
        # type: (List[Cell]) -> List[Destination]
        while self.pointer < len(self.waypoints):
            waypoint = self.waypoints[self.pointer]

            if waypoint is None:
                self.pointer += 1
                continue

            if len(waypoint) == 2:
                waypoint.append(0.0)

            lat, lng, alt = waypoint
            yield Destination(lat, lng, alt, name="Waypoint at {},{}".format(lat, lng))

            self.pointer += 1

        self.pointer = 0

    def waypoint_add(self, longitude, latitude):
        # type: (float, float) -> None
        self.waypoints.append([longitude, latitude])

    def waypoint_remove(self, index):
        # type: (float, float) -> None
        try:
            self.waypoints[index] = None
        except IndexError:
            pass
