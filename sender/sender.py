import rospy
from std_msgs.msg import String
import time
from commands import InnerCommand, ControlCommands, AutopilotCommands, SendCommandsList


class Sender:
    def send(self):
        pass


class CommandSender(Sender):
    def __init__(self):
        self.command_list = SendCommandsList()

    def send(self):
        i = 0
        control_publisher = rospy.Publisher('/robot_control', String, queue_size=10)
        autopilot_publisher = rospy.Publisher('/autopilot', String, queue_size=10)
        try:
            rate = rospy.Rate(1)
            while not rospy.is_shutdown():
                time.sleep(0.2)
                if self.command_list.get_list():
                    command_object: InnerCommand = self.command_list.pop()
                    if command_object.command_type == ControlCommands:
                        msg = f"{command_object.command_name}:{command_object.command_data}"
                        print("IN CONTROL SENDER")
                        control_publisher.publish(msg)
                        print(f"[SENT] {msg}")
                        rate.sleep()
                    elif command_object.command_type == AutopilotCommands:
                        if (command_object.command_name == 'CREATE_ROUTE') or (
                                command_object.command_name == 'CURRENT_ROUTE'):
                            data_string = ';'.join([str(elem) for elem in command_object.command_data])
                            msg = f"{command_object.command_name}:{data_string}"
                            print("IN AUTOPILOT SENDER")
                            autopilot_publisher.publish(msg)
                            print(f"[SENT] {msg}")
                            rate.sleep()
                        else:
                            msg = f"{command_object.command_name}:{command_object.command_data}"
                            print("IN AUTOPILOT SENDER")
                            autopilot_publisher.publish(msg)
                            print(f"[SENT] {msg}")
                            rate.sleep()

        except Exception as e:
            rospy.logwarn(e)
