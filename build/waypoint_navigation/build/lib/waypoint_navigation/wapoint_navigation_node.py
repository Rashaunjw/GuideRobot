#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import time

class WaypointNavigator(Node):

    def __init__(self):
        super().__init__('waypoint_navigator_node')
        self.navigator = BasicNavigator()

    def create_pose(self, x, y, yaw=0.0):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = 0.0
        pose.pose.orientation.w = 1.0  # Simplified, for zero rotation
        return pose

    def run(self):
        self.navigator.waitUntilNav2Active()

        waypoints = [
            self.create_pose(1.0, 1.0),
            self.create_pose(2.0, 0.0),
            self.create_pose(0.0, -1.0)
        ]

        self.navigator.followWaypoints(waypoints)

        while not self.navigator.isTaskComplete():
            feedback = self.navigator.getFeedback()
            if feedback:
                self.get_logger().info(f"Distance remaining: {feedback.distance_remaining:.2f}")

        result = self.navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            self.get_logger().info("All waypoints reached!")
        else:
            self.get_logger().info("Navigation failed or canceled.")

def main(args=None):
    rclpy.init(args=args)
    navigator = WaypointNavigator()
    navigator.run()
    navigator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
