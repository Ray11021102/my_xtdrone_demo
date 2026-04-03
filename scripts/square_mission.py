#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose

class SquareMission:
    def __init__(self):
        rospy.init_node("square_mission")

        self.cmd_pub = rospy.Publisher(
            "/xtdrone/iris_0/cmd", String, queue_size=10
        )
        self.pose_pub = rospy.Publisher(
            "/xtdrone/iris_0/cmd_pose_enu", Pose, queue_size=10
        )

        rospy.sleep(1.0)

    def publish_cmd(self, text, repeat=40):
        rate = rospy.Rate(20)
        msg = String()
        msg.data = text
        for _ in range(repeat):
            self.cmd_pub.publish(msg)
            rate.sleep()

    def publish_pose(self, x, y, z, duration=8.0):
        rate = rospy.Rate(20)
        pose = Pose()
        pose.position.x = x
        pose.position.y = y
        pose.position.z = z
        pose.orientation.x = 0.0
        pose.orientation.y = 0.0
        pose.orientation.z = 0.0
        pose.orientation.w = 1.0

        repeat = int(duration * 20)
        for _ in range(repeat):
            self.pose_pub.publish(pose)
            rate.sleep()

    def fly_to_point(self, x, y, z, stay_time=8.0):
        rospy.loginfo(f"Fly to point: ({x}, {y}, {z})")
        self.publish_pose(x, y, z, duration=stay_time)

    def run(self):
        rospy.loginfo("Step 1: ARM")
        self.publish_cmd("ARM", repeat=40)
        rospy.sleep(2.0)

        rospy.loginfo("Step 2: TAKEOFF")
        self.publish_cmd("AUTO.TAKEOFF", repeat=40)
        rospy.sleep(8.0)

        rospy.loginfo("Step 3: OFFBOARD")
        self.publish_cmd("OFFBOARD", repeat=40)
        rospy.sleep(2.0)

        rospy.loginfo("Step 4: Fly larger square path")
        waypoints = [
            (0.0, 0.0, 3.0),
            (4.0, 0.0, 3.0),
            (4.0, 4.0, 3.0),
            (0.0, 4.0, 3.0),
            (0.0, 0.0, 3.0),
        ]

        for point in waypoints:
            self.fly_to_point(point[0], point[1], point[2], stay_time=8.0)

        rospy.sleep(2.0)

        rospy.loginfo("Step 5: LAND")
        self.publish_cmd("AUTO.LAND", repeat=40)

        rospy.loginfo("Square mission finished")

if __name__ == "__main__":
    try:
        mission = SquareMission()
        mission.run()
    except rospy.ROSInterruptException:
        pass