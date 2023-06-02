from route import *
from tkinter import *
import numpy as np
from queue import Queue

def check_queue(event):
    msg=Window.queue.get()
    Window.console.configure('1.0', msg+'\n')

class Window:
    root = Tk()
    queue=Queue()
    frame = LabelFrame(root, text='Telemetry')
    img = Image("photo", file="/home/ilya/catkin_ws/src/puk/src/logo-color.png")
    route_map = Canvas(root, width=960, height=540, background="white")
    video_stream = Label(root)
    telemetry = Entry(frame)
    create_route_button = Button(root, text="Create route")
    learn_route_button = Button(root, text="Learn route")
    # x = StringVar()
    # x.set("First coordinate")
    route_coordinate1 = Entry(root)
    route_coordinate1.insert(END, "First coordinate")
    route_coordinate2 = Entry(root)
    route_coordinate2.insert(END, "Second coordinate")
    mode_state = IntVar()
    mode_state.set(3)
    r1 = Radiobutton(text='Remote Mode',
                     variable=mode_state, value=1)
    r2 = Radiobutton(text='Auto Mode',
                     variable=mode_state, value=2)
    r3 = Radiobutton(text='Manual Mode',
                     variable=mode_state, value=3)
    console = Text(root)

    # Create label
    console_label = Label(root, text="Console")
    init_message = "App started."
    root.bind("<<CheckQueue>>", check_queue)

        
    @classmethod
    def run(cls):
        
        cls.root.tk.call('wm', 'iconphoto', cls.root._w, cls.img)
        cls.root.title("Remote Control System")
        cls.root.geometry("1920x1080")
        cls.video_stream.grid(row=0, columnspan=4)
        cls.telemetry.pack(fill=BOTH, expand=1)
        cls.frame.grid(row=1, rowspan=3, column=0, columnspan=4, sticky='nsew')
        cls.create_route_button.grid(pady=20, row=2, column=4, columnspan=2, sticky='ew')
        cls.learn_route_button.grid(pady=20, row=2, column=6, columnspan=2, sticky='ew')
        cls.route_coordinate1.grid(padx=10, pady=20, row=1, column=4, columnspan=2, sticky='ew')
        cls.route_coordinate2.grid(padx=10, row=1, column=6, columnspan=2, sticky='ew')
        cls.r1.grid(row=3, column=4)
        cls.r2.grid(row=3, column=5, columnspan=2)
        cls.r3.grid(row=3, column=7)
        cls.console_label.grid(row=4, columnspan=8, sticky='ew')
        cls.console.insert(END, cls.init_message)
        cls.console.grid(row=5, column=0, columnspan=8, sticky='ew')
        waypoints = []
        add: int = 300
        for i in range(100, 900, 25):
            waypoints.append(GraphicalDot(i, np.sin(i)*200 + add))

        graphic_route = Route('shit route', waypoints)

        for dotik in graphic_route.waypoints:
            cls.route_map.create_oval(dotik.x, dotik.y, dotik.x + 3, dotik.y + 3,
                                      fill=dotik.colour, width=10)
        cls.route_map.grid(row=0, column=4, columnspan=4)
        



        # cls.route_map.place(relx=0.5, rely=0.5, anchor='center')
        # cls.route_coordinate1_x.bind("<Button-1>", cls.__on_click)
        cls.root.mainloop()

    @staticmethod
    def __on_click(event):
        event.widget.delete(0, END)
