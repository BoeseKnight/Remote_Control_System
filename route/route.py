class Route:
    def __init__(self, name, waypoints=None):
        if waypoints is None:
            waypoints = []
        self.name = name
        self.waypoints = waypoints


class RouteBuilder:
    def __init__(self, route: Route):
        self.route = route

    def add_waypoint(self, waypoint):
        self.route.waypoints.append(waypoint)

