from queue import Queue
from tkinter.ttk import Combobox
import encoder
from tkinter import *
import numpy as np
from commands.lists import ThreadSafeMetaSingleton
from control_system.state import ControlSystemState
from route import GraphicalDot, Route, Position, RouteStorage


def app_log(console_function):
    def wrapper(*args, **kwargs):
        console_app = Window()
        data = console_function(*args, **kwargs)
        if data is not None:
            console_app.queue.put(data)
            console_app.root.event_generate("<<CheckQueue>>")
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
        self.telemetry_frame = LabelFrame(self.root, text='Telemetry')
        self.console_frame = LabelFrame(self.root, text='Console')
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
        self.route_config_button = Button(self.root, text="Route Configuration", font="Calibri 17",
                                          command=self.__open_route_config_window)
        self.console = Text(self.console_frame, font="17", state=DISABLED)
        self.init_message = "System started."
        self.root.bind("<<CheckQueue>>", self.__check_queue)
        self.root.bind("<<FramesQueue>>", self.__check_frames_queue)

    def run(self):
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.img)
        self.root.title("Remote Control System")
        self.root.geometry("1920x1080")
        self.video_stream.grid(row=0, columnspan=4, sticky='nsew')
        self.telemetry.pack(fill=BOTH, expand=1)
        self.console.pack(fill=BOTH, expand=1)
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
        self.console_frame.grid(row=5, column=0, columnspan=8, sticky='nsew')
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
        self.console.configure(state=DISABLED)

    def __check_frames_queue(self, event):
        photo = self.frames_queue.get()
        self.video_stream.configure(image=photo)
        self.video_stream.image = photo

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
            en = encoder.commands_encoder.CommandEncoder()
            en.set_command(route)
            en.encode_command()
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
            self.system.control_mode = int(self.mode_state.get())
            if self.system.control_mode == "AUTO":
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
            route_index = routes_list_box.current()
            routes_list.pop(route_index)
            routes_list_box.set('')
            routes_list_box.configure(values=routes_list)
            system_routes = self.system.existing_routes
            system_routes.pop(route_index)
            RouteStorage.save_route_list(system_routes)
            self.system.update_routes()

        route_config_window = Toplevel()
        route_config_window.title("Route Configuration")
        route_config_window.geometry("600x800")
        routes_label = Label(route_config_window, text="Routes", font='Calibri 24')
        clear_routes_button = Button(route_config_window, text='Clear route list', font='Calibri 18',
                                     command=clear_routes)
        delete_route_button = Button(route_config_window, text='Delete route', font='Calibri 18',
                                     command=delete_route)
        routes_list = [repr(route) for route in self.system.existing_routes]
        routes_list_box = Combobox(route_config_window, values=routes_list, font="Calibri 20", justify='center',
                                   state='readonly', background='blue')
        self.root.option_add('*TCombobox*Listbox.font', ("Calibri", 20))
        self.root.option_add('*TCombobox*Listbox.Justify', 'center')
        routes_label.pack(fill=X)
        routes_list_box.pack(fill=X)
        clear_routes_button.pack(fill=X)
        delete_route_button.pack(fill=X)
        route_config_window.grab_set()
