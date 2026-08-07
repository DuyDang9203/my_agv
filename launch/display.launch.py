from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_path = os.path.join(get_package_share_directory('my_agv'))
    urdf_file = os.path.join(pkg_path, 'urdf', 'agv.urdf.xacro')
    
    # 1. KHAI BÁO ĐƯỜNG DẪN TỚI FILE CẤU HÌNH RVIZ CỦA EM
    rviz_config_file = os.path.join(pkg_path, 'rviz', 'agv.rviz')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            # 2. THÊM ARGUMENT ĐỂ RVIZ TỰ ĐỘNG LOAD FILE CONFIG NÀY
            arguments=['-d', rviz_config_file]
        )
    ])