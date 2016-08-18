from datetime import datetime
import googlemaps

from pokemongo_bot.navigation.path_finder.path_finder import PathFinder

from app import kernel


@kernel.container.register('google_path_finder', ['@config.core', '@google_maps'])
class GooglePathFinder(PathFinder):

    def __init__(self, config, google_maps):
        super(GooglePathFinder, self).__init__(config)

        self.google_maps = google_maps

    def path(self, from_lat, form_lng, to_lat, to_lng):
        # type: (float, float, float, float) -> List[(float, float)]
        now = datetime.now()
        start = "{},{}".format(from_lat, form_lng)
        end = "{},{}".format(to_lat, to_lng)
        directions_result = self.google_maps.directions(start, end, mode="walking", departure_time=now)

        if len(directions_result) and len(directions_result[0]["legs"]):
            steps = []
            for leg in directions_result[0]["legs"]:
                for step in leg["steps"]:
                    steps.append((step["end_location"]["lat"], step["end_location"]["lng"]))

            # Finally, walk to the stop's exact location as google can snap it's destinations to the
            # nearest road/path/address
            steps.append((to_lat, to_lng))

            return steps
        else:
            # If google doesn't know the way, then we just have to go as the crow flies
            return [
                (to_lat, to_lng)
            ]
