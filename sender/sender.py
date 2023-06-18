import rospy
from std_msgs.msg import String
import time
from commands import InnerCommand, ControlCommands, RouteCommands, SendCommandsList


class Sender:
    def send(self):
        pass


class CommandSender(Sender):
    def __init__(self):
        self.command_list = SendCommandsList()

    def send(self):
        i = 0
        control_publisher = rospy.Publisher('/console_joy_control', String, queue_size=10)
        route_publisher = rospy.Publisher('/route_commands', String, queue_size=10)
        try:
            rate = rospy.Rate(1)
            while not rospy.is_shutdown():
                time.sleep(0.5)
                if self.command_list.get_list():
                    command_object: InnerCommand = self.command_list.pop()
                    if command_object.command_type == ControlCommands:
                        msg = f"{command_object.command_name}:{command_object.command_data}"
                        print("IN CONTROL SENDER")
                        control_publisher.publish(msg)
                        print(f"[SENT] {msg}")
                        rate.sleep()
                    elif command_object.command_type == RouteCommands:
                        if command_object.command_name == 'CREATE_ROUTE':
                            data_string = ','.join([str(elem) for elem in command_object.command_data])
                            msg = f"{command_object.command_name}:{data_string}"
                            print("IN ROUTE SENDER")
                            route_publisher.publish(msg)
                            print(f"[SENT] {msg}")
                            rate.sleep()
        except Exception as e:
            rospy.logwarn(e)
