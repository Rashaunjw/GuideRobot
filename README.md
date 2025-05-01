# Guide Robot

# Description:
Welcome to our project! This is an interactive guide robot used to help navigate visitors and students around Woods Science Laboratories located in Sewanee TN. We created this program using Python and the ROS 2 framework. 

# Instructions/How to install and run:

Open 6 terminals
1. 	Localization terminal
- ros2 launch turtlebot_navigation localization.launch.py map:=woods_floor1.yaml
2. 	Nav2
- ros2 launch turtlebot4_navigation nav2.launch.py
3. 	Rviz map
- ros2 launch turtlebot4_viz view_navigation.launch.py
4. 	UI terminal
- source install/local_setup.bash
- ros2 run waypoint_navigation search_box_example.py
5. 	Build terminal (if you edit files in VSCode)
- colcon build
6. 	Robot ssh
- ssh (IP address specific to robot) ubuntu@10.97.109.179 
- password: Turtlebot4
- ros2 topic list (to check if robot and laptop are connected)

# How to use: 
The user can type in a room name on the laptop interface and the machine will send the coordinates to the robot. It then will guide the user to the specific room that they input into the interface.
