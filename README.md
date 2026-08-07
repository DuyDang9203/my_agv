# 🤖 my_agv - Differential Drive AMR Simulation Package (ROS 2)

> A ROS 2 simulation package for a Differential Drive Autonomous Mobile Robot (AMR) in Gazebo. The system features multi-sensor fusion (**LiDAR, IMU, Camera**), autonomous navigation using **A\*** and **DWB Planner**, and real-time obstacle avoidance with dynamic obstacles (simulated moving pedestrians).

---

## 🌟 Key Features

- **Kinematic Modeling & Sensor Integration:** Accurate differential drive robot design built via URDF/Xacro, integrating data streams from 2D LiDAR, IMU, and RGB Camera sensors.
- **Path Planning & Navigation (Nav2 Stack):**
  - **Global Planner:** Utilizes the **A\*** algorithm to calculate global optimal trajectories to the target destination.
  - **Local Planner:** Leverages the **DWB Planner** for trajectory tracking and real-time dynamic obstacle avoidance.
- **Dynamic Obstacles:** Features a 3D Gazebo environment integrated with animated pedestrian models (Actors) to test and validate collision-avoidance robustness.
- **SLAM & Localization:** Includes an Extended Kalman Filter (EKF via `robot_localization`) fusing Odometry + IMU data, along with SLAM support for scanning and mapping new environments.

---

## 📂 Package Structure

```text
my_agv/
├── config/              # Parameter files (.yaml, .xml) for Nav2 (A*, DWB), EKF, Bridge
├── data/                # Python scripts for data collection and processing
├── launch/              # Launch scripts (bringup, nav2, slam, gazebo)
├── maps/                # Static map files (.pgm, .yaml) for Navigation
├── models/              # 3D models (dynamic obstacles, animated human Actors)
├── rviz/                # RViz2 visualization configurations (agv.rviz)
├── src/                 # Custom C++ / Python source code
├── test/                # Unit tests
├── urdf/                # Robot description, TF tree, and sensor mountings (agv.urdf.xacro)
├── worlds/              # 3D Gazebo simulation worlds (my_world.sdf, my_world3.sdf)
├── CMakeLists.txt       # ROS 2 build configuration
└── package.xml          # Package manifest and dependency declarations
1. Prerequisites

Ensure you have Ubuntu (22.04 / 24.04), ROS 2, and the required Navigation2 and Gazebo packages installed:
Bash

sudo apt update
sudo apt install ros-$ROS_DISTRO-navigation2 ros-$ROS_DISTRO-nav2-bringup \
                 ros-$ROS_DISTRO-robot-localization ros-$ROS_DISTRO-slam-toolbox -y

2. Building the Package

Navigate to your ROS 2 workspace and build my_agv:
Bash

cd ~/Documents/robot_ws
colcon build --packages-select my_agv --symlink-install
source install/setup.bash

🚀 How to Run

Execution follows a two-step workflow: first launch bringup to load the robot and simulation environment, then launch nav2 (navigation) or slam (mapping).
Step 1: Launch Robot & Gazebo Simulation (Terminal 1)
Bash

ros2 launch my_agv bringup.launch.py

Step 2: Choose Operation Mode (Terminal 2)
🟢 Mode A: Navigation & Obstacle Avoidance

Launch the Navigation2 stack using pre-built maps:
Bash

ros2 launch my_agv nav2.launch.py

Use the 2D Goal Pose tool in RViz2 to assign target destinations for the AGV.
🟢 Mode B: SLAM / Mapping

To map a new environment from scratch:
Bash

ros2 launch my_agv slam.launch.py

👨‍💻 Author

    Dang Quang Duy - Mechatronics & Robotics Engineer

    Repository: https://github.com/DuyDang9203/my_agv