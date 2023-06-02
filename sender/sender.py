import rospy
from std_msgs.msg import String
from commands import *


class Sender:
    def send(self):
        pass


class CommandSender(Sender):
    def __init__(self):
        self.command_list = SendCommandsList()

    def send(self):
        i = 0
        pub = rospy.Publisher('/console_joy_control', String, queue_size=10)
        try:
            rate = rospy.Rate(1)
            while not rospy.is_shutdown():
                if self.command_list.get_list():
                    msg_object : InnerCommand=self.command_list.pop()
                    msg=f"{msg_object.command_name}:{msg_object.command_data}" 
                    print("IN SENDER")
                    # i += 1
                    # msg = "respond" + str(i)
                    # pub.publish(msg)
                    # print(f"[SENT] {msg}")
                    # rate.sleep()
                    pub.publish(msg)
                    print(f"[SENT] {msg}")
                    rate.sleep()
        except Exception as e:
            rospy.logwarn(e)
