import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # 1. Lấy đường dẫn gói slam_toolbox gốc từ hệ thống ROS 2 Jazzy
    pkg_slam_toolbox = get_package_share_directory("slam_toolbox")

    # 2. Định nghĩa tham số thời gian mô phỏng
    use_sim_time = LaunchConfiguration("use_sim_time", default="True")

    # 3. Gọi file cấu hình quét bản đồ trực tuyến không đồng bộ (Online Async)
    # Đây là chế độ quét tối ưu và nhẹ nhất cho xe AGV di chuyển tự do
    slam_toolbox_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_slam_toolbox, "launch", "online_async_launch.py")
        ),
        launch_arguments={"use_sim_time": use_sim_time}.items(),
    )

    # 4. Trả về thực thi nạp lệnh
    ld = LaunchDescription()
    ld.add_action(slam_toolbox_cmd)

    return ld