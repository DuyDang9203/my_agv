import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():
    # 1. Định nghĩa các package liên quan
    pkg_my_agv = get_package_share_directory("my_agv")
    pkg_nav2_bringup = get_package_share_directory("nav2_bringup")

    # 2. Định nghĩa thư mục chứa các tệp bản đồ và file tham số mặc định
    maps_dir = os.path.join(pkg_my_agv, "maps")
    default_params_path = os.path.join(pkg_my_agv, "config", "nav2_params.yaml")

    # 3. Khai báo các Launch Configuration để hứng tham số từ Terminal
    map_name_config = LaunchConfiguration("map_name") # Hứng tên file map
    params_config = LaunchConfiguration("params_file")
    use_sim_time_config = LaunchConfiguration("use_sim_time")

    # =========================================================================
    # 4. KHAI BÁO CÁC BIẾN ĐẦU VÀO (Chỉ truyền TÊN FILE bản đồ)
    # =========================================================================
    declare_map_name_cmd = DeclareLaunchArgument(
        "map_name",
        default_value="my_factory_map.yaml", # Tên map mặc định nếu không truyền gì
        description="Chỉ cần gõ tên file map nằm trong thư mục my_agv/maps/",
    )

    declare_params_cmd = DeclareLaunchArgument(
        "params_file",
        default_value=default_params_path,
        description="Đường dẫn tuyệt đối đến tệp cấu hình Nav2 YAML",
    )

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time",
        default_value="True",
        description="Sử dụng thời gian mô phỏng (True/False)",
    )

    # 🌟 GỘP ĐỘNG: Tự động nối [Đường dẫn thư mục maps] + [Tên file map em nhập từ terminal]
    full_map_path = PathJoinSubstitution([maps_dir, map_name_config])
    # =========================================================================

    # 5. Gọi file bringup_launch.py tổng hợp của hệ thống
    nav2_bringup_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_bringup, "launch", "bringup_launch.py")
        ),
        launch_arguments={
            "map": full_map_path,          # Truyền đường dẫn đầy đủ sau khi gộp động
            "params_file": params_config,
            "use_sim_time": use_sim_time_config,
            "autostart": "True",
            "use_velocity_smoother": "true",
            "use_collision_monitor": "False",
            "use_robot_state_pub": "False",
        }.items(),
    )

    # 6. Nạp tất cả lệnh khai báo tham số và thực thi vào LaunchDescription
    ld = LaunchDescription()

    ld.add_action(declare_map_name_cmd)
    ld.add_action(declare_params_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(nav2_bringup_cmd)

    return ld