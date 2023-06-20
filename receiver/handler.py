from control_system.state import ControlSystemState
from decoder import CommandDecoder
from window.main_window import tech_view_log, telemetry_log


class HandlerProvider:
    def __init__(self):
        self.topics_handlers = {'telemetry': TelemetryHandler(), 'tech_view': TechViewHandler()}

    def get_handler(self, topic):
        return self.topics_handlers.get(topic)


class TopicHandler:
    def __init__(self):
        self.system = ControlSystemState()
        self.decoder = CommandDecoder()

    def run(self, data):
        pass


class TelemetryHandler(TopicHandler):
    @telemetry_log
    def run(self, data):
        tele = data.split('|')
        print(f'{data} in {type(self)}')
        return f'{tele[0]}\n{tele[1]}\n{tele[2]}'


class TechViewHandler(TopicHandler):
    @tech_view_log
    def run(self, data):
        print(f'{data} in {type(self)}')
        return data
