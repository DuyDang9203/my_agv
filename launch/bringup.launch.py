import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess, SetEnvironmentVariable 
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_path = get_package_share_directory('my_agv')
    urdf_file = os.path.join(pkg_path, 'urdf', 'agv.urdf.xacro')
    rviz_config_file = os.path.join(pkg_path, 'rviz', 'agv.rviz')

    doc = xacro.process_file(urdf_file)
    robot_desc = doc.toxml()

    # Đường dẫn tới các file cấu hình
    bridge_config_file = os.path.join(pkg_path, 'config', 'bridge_config.yaml')
    ekf_config_file = os.path.join(pkg_path, 'config', 'ekf.yaml') 

    # 1. Khởi động môi trường Gazebo
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    world_path = os.path.join(pkg_path, 'worlds', 'my_world.sdf')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', world_path]}.items(),
    )

    # 2. Phát thông tin trạng thái xe (Robot State Publisher)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_desc, 
            'use_sim_time': True
        }]
    )

    # 3. Tự động thả xe (Spawn) vào Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_agv',
            '-topic', 'robot_description',
            '-x', '2.0',    
            '-y', '2.0',    
            '-z', '0.2',    
            '-Y', '0.0'     
        ],
        output='screen'
    )

    # 4. Mạch cầu nối tín hiệu ROS 2 <-> Gazebo (Nhận thêm dữ liệu IMU)
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_config_file,
            'use_sim_time': True
        }],
        output='screen'
    )

    # 5. Mở RViz2 với cấu hình đã lưu
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{
            'use_sim_time': True
        }],
        output='screen'
    )

   # 6. Node trung chuyển thông số khớp bánh xe
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{
            'source_list': ['/joint_states'], 
            'use_sim_time': True
        }]
    )
    # =========================================================================
    # 7. THÊM NODE ROBOT_LOCALIZATION (Bộ lọc EKF)
    # =========================================================================
    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config_file, {'use_sim_time': True}]
    )

    # =========================================================================
    # TÍCH HỢP ĐOẠN GỌI THUẬT TOÁN SLAM_TOOLBOX
    # =========================================================================
    pkg_slam_toolbox = get_package_share_directory('slam_toolbox')
    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_slam_toolbox, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={'use_sim_time': 'True'}.items(),
    )

    return LaunchDescription([
        # =========================================================================
        # ÉP CẤU HÌNH ĐỒ HỌA CHẠY PHẦN MỀM (SOFTWARE RENDER) ĐỂ SỬA LỖI ĐƠ DRIVER NVIDIA
        # =========================================================================
        SetEnvironmentVariable(name='__NV_PRIME_RENDER_OFFLOAD', value='1'),
        SetEnvironmentVariable(name='__GLX_VENDOR_LIBRARY_NAME', value='nvidia'),
        # =========================================================================

        gazebo,
        robot_state_publisher,
        joint_state_publisher,
        bridge,
        robot_localization_node,
        rviz,
        #slam_toolbox, 

        # Thả xe trễ 5 giây
        TimerAction(
            period=5.0,
            actions=[spawn_entity]
        ),
    ])
    