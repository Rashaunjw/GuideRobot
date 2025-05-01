#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import subprocess

class SoundPlayer(Node):
    def __init__(self):
        super().__init__('sound_player')
        self.subscription = self.create_subscription(
            String,
            'play_sound',
            self.listener_callback,
            10
        )
        self.get_logger().info("Sound player node ready.")

    def listener_callback(self, msg):
        sound_map = {
            "goodbye": "/home/ubuntu/goodbye.wav",
        }

        sound_file = sound_map.get(msg.data)
        if sound_file:
            self.get_logger().info(f"Playing sound: {msg.data}")
            try:
                subprocess.run(["/usr/bin/aplay", sound_file], check=True)
            except Exception as e:
                self.get_logger().error(f"Error playing sound: {e}")
        else:
            self.get_logger().warn(f"Unknown sound requested: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = SoundPlayer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
