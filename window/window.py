from route import *
from tkinter import *


class Window:
    __root = Tk()
    img = Image("photo", file="/home/ilya/catkin_ws/src/puk/src/logo-color.png")
    route_map = Canvas(__root, width=960, height=540, background="white")
    video_stream = Label(__root)
    create_route_button = Button(__root, text="Create route")
    # x = StringVar()
    # x.set("First coordinate")
    route_coordinate1 = Entry(__root)
    route_coordinate1.insert(END, "First coordinate")
    route_coordinate2 = Entry(__root)
    route_coordinate2.insert(END, "Second coordinate")
    mode_state = IntVar()
    mode_state.set(3)
    r1 = Radiobutton(text='Remote Mode',
                     variable=mode_state, value=1)
    r2 = Radiobutton(text='Auto Mode',
                     variable=mode_state, value=2)
    r3 = Radiobutton(text='Manual Mode',
                     variable=mode_state, value=3)

    @classmethod
    def run(cls):
        cls.__root.tk.call('wm','iconphoto',cls.__root._w,cls.img)
        cls.__root.title("Remote Control System")
        cls.__root.geometry("1920x1080")
        cls.route_map.grid(pady=20, row=0, column=4, columnspan=4)
        cls.video_stream.grid(row=0, columnspan=4)
        cls.create_route_button.grid(pady=20, row=2, column=5, columnspan=2, sticky='ew')
        cls.route_coordinate1.grid(padx=10, pady=20, row=1, column=4, columnspan=2, sticky='ew')
        cls.route_coordinate2.grid(padx=10, row=1, column=6, columnspan=2, sticky='ew')
        cls.r1.grid(row=3, column=4)
        cls.r2.grid(row=3, column=5, columnspan=2)
        cls.r3.grid(row=3, column=7)
        # cls.route_coordinate1_x.bind("<Button-1>", cls.__on_click)
        cls.__root.mainloop()

        # waypoints = []
        # for i in range(6, 300, 10):
        #     waypoints.append(GraphicalDot(i, i))
        #
        # graphic_route = Route('shit route', waypoints)

        #
        # for dot in graphic_route.waypoints:
        #     cls.route_map.create_oval(dot.x, dot.y, dot.x + 3, dot.y + 3,
        #                               fill=dot.colour, width=10)

        # route_map.place(relx=0.5, rely=0.5, anchor='center')
    @staticmethod
    def __on_click(event):
        event.widget.delete(0, END)
