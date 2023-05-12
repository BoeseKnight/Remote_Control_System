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
        pub = rospy.Publisher('/route_cmds_response', String, queue_size=10)
        try:
            rate = rospy.Rate(1)
            while not rospy.is_shutdown():
                i += 1
                msg = "respond" + str(i)
                pub.publish(msg)
                print(f"[SENT] {msg}")
                rate.sleep()
        except Exception as e:
            rospy.logwarn(e)
