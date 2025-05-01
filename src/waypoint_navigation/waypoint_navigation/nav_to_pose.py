import rclpy

from turtlebot4_navigation.turtlebot4_navigator import TurtleBot4Directions, TurtleBot4Navigator

def main():
    rclpy.init()

    navigator = TurtleBot4Navigator()

    a = input("Where would you like to go? ")

    if a == "door":
        goal_pose = navigator.getPoseStamped([.179,-.05], TurtleBot4Directions.EAST)
    elif a == "other":
        goal_pose = navigator.getPoseStamped([-7.71, -3.81], TurtleBot4Directions.EAST)
    else:
        pass

    

    navigator.startToPose(goal_pose)

    rclpy.shutdown()

if __name__ == '__main__':
    main()