from queue import Queue
from tkinter.ttk import Combobox
import encoder
from tkinter import *
import numpy as np
from commands.lists import ThreadSafeMetaSingleton
from commands.command import AutopilotCommands
from control_system.state import ControlSystemState
from route import GraphicalDot, Route, Position, RouteStorage
from gamepad.control_configuration import ControlConfiguration, ControlsFile
from gamepad.gamepad_buttons import GamepadButtons


def app_log(console_function):
    def wrapper(*args, **kwargs):
        console_app = Window()
        data = console_function(*args, **kwargs)
        if data is not None:
            console_app.queue.put(data)
            console_app.root.event_generate("<<CheckQueue>>")
        return data

    return wrapper


def tech_view_log(tech_view_function):
    def wrapper(*args, **kwargs):
        console_app = Window()
        data = tech_view_function(*args, **kwargs)
        print("IN TECH LOG")
        if data is not None:
            console_app.tech_view_queue.put(data)
            console_app.root.event_generate("<<TechViewQueue>>")
        return data

    return wrapper


def telemetry_log(telemetry_function):
    def wrapper(*args, **kwargs):
        console_app = Window()
        data = telemetry_function(*args, **kwargs)
        print("IN TELEMETRY LOG")
        if data is not None:
            console_app.telemetry_queue.put(data)
            console_app.root.event_generate("<<TelemetryQueue>>")
        return data

    return wrapper


class Window(metaclass=ThreadSafeMetaSingleton):
    system = ControlSystemState()

    def __init__(self):
        self.root = Tk()
        # self.root.resizable(False, False)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)
        self.root.columnconfigure(0, weight=100)

        self.queue = Queue()
        self.frames_queue = Queue()
        self.tech_view_queue = Queue()
        self.telemetry_queue = Queue()
        self.command_encoder = encoder.commands_encoder.CommandEncoder()

        self.telemetry_frame = LabelFrame(self.root, text='Telemetry')
        self.console_frame = LabelFrame(self.root, text='Console')
        self.tech_view_console_frame = LabelFrame(self.root, text='Tech View Console')

        self.img = Image("photo", file="/home/ilya/catkin_ws/src/puk/src/logo-color.png")
        self.route_map = Canvas(self.root, width=960, height=540, background="white")
        self.video_stream = Label(self.root)
        self.telemetry = Text(self.telemetry_frame, font="Calibri 24", state=DISABLED)
        self.create_route_button = Button(self.root, text="Create route", font="Calibri 17",
                                          command=self.__create_route)
        self.learn_route_button = Button(self.root, text="Learn route", bg='red', font="Calibri 17",
                                         activebackground='#ff4c63',
                                         command=self.__learn_route)
        self.route_coordinate1 = Entry(self.root, font="Calibri 24")
        self.route_coordinate1.insert(END, "First coordinate")
        self.route_coordinate1.bind("<Button-1>", self.__route_field_on_click1)
        self.route_coordinate2 = Entry(self.root, font="Calibri 24")
        self.route_coordinate2.insert(END, "Second coordinate")
        self.route_coordinate2.bind("<Button-1>", self.__route_field_on_click2)
        self.mode_state = IntVar()
        self.mode_state.set(1)
        self.r1 = Radiobutton(text='Remote Mode',
                              variable=self.mode_state, value=1, font="Calibri 14", command=self.__mode_on_click)
        self.r2 = Radiobutton(text='Auto Mode',
                              variable=self.mode_state, value=2, font="Calibri 14", command=self.__mode_on_click)
        self.r3 = Radiobutton(text='Manual Mode',
                              variable=self.mode_state, value=3, font="Calibri 14", command=self.__mode_on_click)
        self.route_config_button = Button(self.root, text="Route & Control Configuration", font="Calibri 17",
                                          command=self.__open_route_config_window)
        self.console = Text(self.console_frame, font="17", state=DISABLED)
        self.tech_view_console = Text(self.tech_view_console_frame, font="17", state=DISABLED)
        self.init_message = "System started."
        self.root.bind("<<CheckQueue>>", self.__check_queue)
        self.root.bind("<<FramesQueue>>", self.__check_frames_queue)
        self.root.bind("<<TechViewQueue>>", self.__check_tech_view_queue)
        self.root.bind("<<TelemetryQueue>>", self.__check_telemetry_queue)

    def run(self):
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.img)
        self.root.title("Remote Control System")
        self.root.geometry("1920x1080")
        self.video_stream.grid(row=0, columnspan=4, sticky='nsew')
        self.telemetry.pack(fill=BOTH, expand=1)
        self.console.pack(fill=BOTH, expand=1)
        self.tech_view_console.pack(fill=BOTH, expand=1)
        self.telemetry_frame.grid(row=1, pady=3, rowspan=4, column=0, columnspan=4, sticky='nsew')
        self.route_coordinate1.grid(padx=10, pady=3, row=1, column=4, columnspan=2, sticky='nsew')
        self.route_coordinate2.grid(padx=10, pady=3, row=1, column=6, columnspan=2, sticky='nsew')
        self.create_route_button.grid(padx=10, pady=3, row=2, column=4, columnspan=2, sticky='nsew')
        self.learn_route_button.grid(padx=10, pady=3, row=2, column=6, columnspan=2, sticky='nsew')
        self.r1.grid(row=3, column=4, sticky='nsew')
        self.r2.grid(row=3, column=5, columnspan=2, sticky='nsew')
        self.r3.grid(row=3, column=7, sticky='nsew')
        self.route_config_button.grid(row=4, column=4, columnspan=4, padx=10, pady=3, sticky='nsew')
        self.console.insert(END, self.init_message)
        self.console_frame.grid(row=5, column=0, columnspan=4, sticky='nsew')
        self.tech_view_console_frame.grid(row=5, column=4, columnspan=4, sticky='nsew')

        # self.console.grid()
        waypoints = []
        add: int = 300
        for i in range(100, 900, 25):
            waypoints.append(GraphicalDot(i, np.sin(i) * 200 + add))

        graphic_route = Route('shit route', waypoints)

        for dotik in graphic_route.waypoints:
            self.route_map.create_oval(dotik.x, dotik.y, dotik.x + 3, dotik.y + 3,
                                       fill=dotik.colour, width=10)
        self.route_map.grid(row=0, column=4, columnspan=4, sticky='nsew')

        self.root.mainloop()

    def __check_queue(self, event):
        msg = self.queue.get()
        self.console.configure(state=NORMAL)
        self.console.insert('1.0', f"{msg}\n")
        if msg == 'Learning mode is OFF':
            self.console.tag_add('red', '1.0', '1.end')
            self.console.tag_config('red', foreground='red')
        self.console.configure(state=DISABLED)

    def __check_tech_view_queue(self, event):
        msg: str = self.tech_view_queue.get()
        command_name, args = msg.split(':')
        log_message = f'[{command_name}]:{args}'
        self.tech_view_console.configure(state=NORMAL)
        self.tech_view_console.insert('1.0', f"{log_message}\n")
        if command_name == 'CRITICAL_WARNING':
            if self.system.control_mode == 'AUTO':
                self.mode_state.set(1)
                self.__mode_on_click()
            self.tech_view_console.tag_add('red', '1.0', '1.end')
            self.tech_view_console.tag_config('red', foreground='red')
        self.tech_view_console.configure(state=DISABLED)

    def __check_frames_queue(self, event):
        photo = self.frames_queue.get()
        self.video_stream.configure(image=photo)
        self.video_stream.image = photo

    def __check_telemetry_queue(self, event):
        msg = self.telemetry_queue.get()
        self.telemetry.configure(state=NORMAL)
        self.telemetry.delete('1.0', 'end')
        self.telemetry.insert('1.0', f"{msg}\n")
        self.console.configure(state=DISABLED)

    @app_log
    def __create_route(self):
        try:
            coordinate1 = [float(i) for i in self.route_coordinate1.get().split(';')]
            coordinate2 = [float(i) for i in self.route_coordinate2.get().split(';')]

            position1 = Position(coordinate1[0], coordinate1[1], coordinate1[2])
            position2 = Position(coordinate2[0], coordinate2[1], coordinate2[2])
            route = Route("test", [position1, position2])
            RouteStorage.save_route(route)
            self.system.update_routes()
            self.command_encoder.set_command((AutopilotCommands.CREATE_ROUTE, route.waypoints))
            self.command_encoder.encode_command()
            # save route
            return route
        except Exception as e:
            print(e)
            return 'Entered coordinates not correct'
        finally:
            self.route_coordinate1.delete(0, END)
            self.route_coordinate2.delete(0, END)
            self.route_coordinate1.insert(END, "First coordinate")
            self.route_coordinate2.insert(END, "Second coordinate")

    def __route_field_on_click1(self, event):
        self.route_coordinate1.delete(0, END)

    def __route_field_on_click2(self, event):
        self.route_coordinate2.delete(0, END)

    @app_log
    def __mode_on_click(self):
        if self.system.mode_is_set(int(self.mode_state.get())) is False:
            if self.system.control_mode == "AUTO":
                self.command_encoder.set_command((AutopilotCommands.MODE, 'OFF'))
                self.command_encoder.encode_command()
            self.system.control_mode = int(self.mode_state.get())
            if self.system.control_mode == "AUTO":
                self.command_encoder.set_command((AutopilotCommands.MODE, 'ON'))
                self.command_encoder.encode_command()
                self.learn_route_button.configure(state=DISABLED, background="#D3D3D3")
            else:
                self.system.is_learning = 0
                self.__change_learn_button_colour()
                self.learn_route_button.configure(state=NORMAL)
            return f'Control Mode: {self.system.control_mode}'

    @app_log
    def __learn_route(self):
        self.system.is_learning = 1
        is_on = 'ON' if self.system.is_learning == 1 else 'OFF'
        self.command_encoder.set_command((AutopilotCommands.LEARN_ROUTE, is_on))
        self.command_encoder.encode_command()
        route = Route(name="Learning route")
        self.system.learning_route = route
        self.__change_learn_button_colour()
        return f'Learning mode is {is_on}'

    def __change_learn_button_colour(self):
        color = "#33b249" if self.system.is_learning == 1 else "#ff0021"
        active_color = "#70c97f" if self.system.is_learning == 1 else "#ff4c63"
        self.learn_route_button.configure(background=color, activebackground=active_color)

    def __open_route_config_window(self):
        def clear_routes():
            RouteStorage.clear_routes()
            self.system.update_routes()
            print('shit')
            routes_list_box.configure(values=())

        def delete_route():
            try:
                route_index = routes_list_box.current()
                routes_list.pop(route_index)
                routes_list_box.set('')
                self.command_encoder.set_command((AutopilotCommands.DELETE_ROUTE, str(route_index)))
                self.command_encoder.encode_command()
                routes_list_box.configure(values=routes_list)
                system_routes = self.system.existing_routes
                system_routes.pop(route_index)
                RouteStorage.save_route_list(system_routes)
                self.system.update_routes()
            except Exception:
                print("ERROR DELETING ROUTE")

        def select_route():
            try:
                route_index = routes_list_box.current()
                if route_index >= 0:
                    routes_list_box.set('')
                    # system_routes: list = self.system.existing_routes
                    # current_route = system_routes[route_index]
                    # print(current_route)
                    self.command_encoder.set_command((AutopilotCommands.CURRENT_ROUTE, str(route_index)))
                    self.command_encoder.encode_command()
            except Exception as e:
                print("ERROR SELECTING ROUTE" + str(e))

        route_config_window = Toplevel()
        route_config_window.title("Route Configuration")
        route_config_window.geometry("600x800")
        routes_label = Label(route_config_window, text="Routes", font='Calibri 24')
        select_route_button = Button(route_config_window, text='Select route', font='Calibri 18',
                                     command=select_route)
        clear_routes_button = Button(route_config_window, text='Clear route list', font='Calibri 18',
                                     command=clear_routes)
        delete_route_button = Button(route_config_window, text='Delete route', font='Calibri 18',
                                     command=delete_route)
        routes_list = [repr(route) for route in self.system.existing_routes]
        routes_list_box = Combobox(route_config_window, values=routes_list, font="Calibri 20", justify='center',
                                   state='readonly', background='blue')
        controls_label = Label(route_config_window, text="Controls", font='Calibri 24')
        self.root.option_add('*TCombobox*Listbox.font', ("Calibri", 20))
        self.root.option_add('*TCombobox*Listbox.Justify', 'center')
        routes_label.pack(fill=X)
        routes_list_box.pack(fill=X)
        select_route_button.pack(fill=X)
        clear_routes_button.pack(fill=X)
        delete_route_button.pack(fill=X)

        controls_label.pack(pady=20, fill=X)
        labels_dict = {}
        combobox_dict = {}
        controls_frame = Frame(route_config_window)
        config = list(self.system.control_configuration.keys())
        for index, (key, value) in enumerate(self.system.control_configuration.items()):

            @app_log
            def create_config():
                try:
                    print(f'OLD: {self.system.control_configuration}')
                    emptiness_check = config.index('')
                    return 'Fulfill all control fields'
                except ValueError:
                    new_config = ControlConfiguration(config)
                    self.system.control_configuration = ControlsFile.read_configuration()
                    print(f'NEW: {self.system.control_configuration}')
                    return 'Control configuration created'

            def select_control(event, x=index):
                control = event.widget.get()
                print(f'{control} {x}')
                try:
                    repeated_element = config.index(control)
                    if repeated_element != x:
                        print(f'in try {repeated_element}')
                        config[repeated_element] = ''
                        combobox_dict[repeated_element].set('')
                except ValueError:
                    pass
                config[x] = control
                # config.insert(x, event.widget.get())
                print(config)
                repeated_element = -1

            labels_dict[value] = Label(controls_frame, text=value, font="Calibri 20", )
            labels_dict[value].grid(row=index, column=0)
            combobox_dict[index] = Combobox(controls_frame, values=list([button.name for button in GamepadButtons]),
                                            font="Calibri 20", justify='center',
                                            state='readonly', background='blue')
            index_set = list([button.name for button in GamepadButtons]).index(key)
            combobox_dict[index].current(index_set)
            combobox_dict[index].grid(row=index, column=1)
            combobox_dict[index].bind('<<ComboboxSelected>>', select_control)
        controls_frame.pack()
        create_configuration_button = Button(route_config_window, text='Create configuration', font='Calibri 18',
                                             command=create_config)
        create_configuration_button.pack(pady=10, fill=X)
        route_config_window.grab_set()
