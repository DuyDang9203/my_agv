#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import Twist
import csv
import os

class DataRecorder(Node):
    def __init__(self):
        super().__init__('data_recorder_node')
        
        self.data_dir = os.path.dirname(os.path.realpath(__file__))
        
        self.odom_file_path = os.path.join(self.data_dir, 'bao_cao_vi_tri_odom.csv')
        self.cmd_vel_file_path = os.path.join(self.data_dir, 'bao_cao_van_toc_dwb.csv')
        self.plan_file_path = os.path.join(self.data_dir, 'bao_cao_ke_hoach_plan.csv')
        
        self.init_csv_files()

        # Chỉ đăng ký các Subscriber cốt lõi
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.cmd_vel_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.plan_sub = self.create_subscription(Path, '/plan', self.plan_callback, 10)
        
        self.get_logger().info('=====================================================')
        self.get_logger().info('Dang ghi dữ liệu: Toạ độ X-Y, Vận tốc thực vs Vận tốc lệnh...')
        self.get_logger().info('=====================================================')

    def init_csv_files(self):
        # File Odom: Chỉ giữ lại tọa độ và vận tốc thực tế của thân xe (V_real, W_real)
        with open(self.odom_file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'X', 'Y', 'V_real', 'W_real'])
            
        # File Cmd_vel: Chỉ giữ lại vận tốc lệnh phát từ DWB (V_cmd, W_cmd)
        with open(self.cmd_vel_file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'V_cmd', 'W_cmd'])

        # File Plan: Giữ lại đường lập kế hoạch ban đầu từ A*
        with open(self.plan_file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'X_plan', 'Y_plan'])

    def odom_callback(self, msg):
        timestamp = self.get_clock().now().to_msg().sec + self.get_clock().now().to_msg().nanosec * 1e-9
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        v = msg.twist.twist.linear.x
        w = msg.twist.twist.angular.z
        
        with open(self.odom_file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, x, y, v, w])

    def cmd_vel_callback(self, msg):
        timestamp = self.get_clock().now().to_msg().sec + self.get_clock().now().to_msg().nanosec * 1e-9
        v_cmd = msg.linear.x
        w_cmd = msg.angular.z
        
        with open(self.cmd_vel_file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, v_cmd, w_cmd])

    def plan_callback(self, msg):
        timestamp = self.get_clock().now().to_msg().sec + self.get_clock().now().to_msg().nanosec * 1e-9
        with open(self.plan_file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for pose_stamped in msg.poses:
                writer.writerow([timestamp, pose_stamped.pose.position.x, pose_stamped.pose.position.y])

def main(args=None):
    rclpy.init(args=args)
    node = DataRecorder()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Da dung ghi du lieu!')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()