import rospy
from std_msgs.msg import String

i = 0


class Test1:
    @classmethod
    def print_shit(cls):
        print("shit")


class Receiver:
    @classmethod
    def receive(cls):
        rospy.Subscriber("route_cmds", String, cls.callback)
        rospy.spin()

    @classmethod
    def callback(cls, data):
        Test1.print_shit()
        global i
        i += 1
        # rospy.loginfo(rospy.get_caller_id() + "I hears %s", data.data)
        print(data.data + str(i))


class Sender:
    @classmethod
    def send(cls):
        i=0
        pub = rospy.Publisher('/route_cmds_response', String, queue_size=10)
        try:
        # For debugging
            rate = rospy.Rate(1)
            while not rospy.is_shutdown():
                i+=1
                msg="respond"+str(i)
                pub.publish(msg)
                print(f"[SENT] {msg}")
                rate.sleep()

        except Exception as e:
            rospy.logwarn(e)

    @classmethod
    def callback(cls, data):
        Test1.print_shit()
        global i
        i += 1
        # rospy.loginfo(rospy.get_caller_id() + "I hears %s", data.data)
        print(data.data + str(i))
