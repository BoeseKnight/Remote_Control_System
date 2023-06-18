import pickle


class Route:
    def __init__(self, name, waypoints=None):
        if waypoints is None:
            waypoints = []
        self.name = name
        self.waypoints = waypoints

    def __repr__(self):
        return f"{self.name} : {self.waypoints}"


class RouteBuilder:
    def __init__(self, route: Route):
        self.route = route

    def add_waypoint(self, waypoint):
        self.route.waypoints.append(waypoint)


class RouteStorage:
    file_path = '/home/ilya/catkin_ws/src/puk/src/route/route_storage.txt'

    @classmethod
    def save_route(cls, route: Route):
        with open(cls.file_path, 'ab') as file_output:
            pickle.dump(route, file_output, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def save_route_list(cls, routes: list):
        with open(cls.file_path, 'wb') as file_output:
            for route in routes:
                pickle.dump(route, file_output, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def read_routes(cls):
        routes_list = []
        with open(cls.file_path, 'rb') as file_input:
            while True:
                try:
                    route_object = pickle.load(file_input)
                    routes_list.append(route_object)
                    print(route_object)
                except Exception:
                    break
        return routes_list

    @classmethod
    def clear_routes(cls):
        with open(cls.file_path, 'wb') as file:
            pass
