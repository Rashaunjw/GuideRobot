from setuptools import find_packages, setup

package_name = 'waypoint_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='student',
    maintainer_email='student@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'waypoint_navigation_node = waypoint_navigation.waypoint_navigation_node:main',
            'nav_to_pose = waypoint_navigation.nav_to_pose:main',
            'search_box_example = waypoint_navigation.search_box_example:main',
            'our_waypoint = waypoint_navigation.our_waypoint:main',
            'waypoint_lights = waypoint_navigation.waypoint_lights:main',
            'sound_player_node = waypoint_navigation.sound_player_node:main'
        ],
    },
)
