#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from nav_msgs.msg import Path
import math
import sys

class GoalErrorCalculator(Node):
    def __init__(self):
        super().__init__('goal_error_calculator')
        
        self.goal_x = None
        self.goal_y = None
        self.goal_yaw = None
        self.estimated_distance = 0.0
        
        # 1. Nhận điểm đích từ RViz
        self.sub_goal = self.create_subscription(
            PoseStamped, 
            '/goal_pose', 
            self.goal_callback, 
            10)
            
        # 2. Nhận vị trí thực tế của xe từ AMCL
        self.sub_pose = self.create_subscription(
            PoseWithCovarianceStamped, 
            '/amcl_pose', 
            self.pose_callback, 
            10)
            
        # 3. Lắng nghe đường dẫn (path) để tính tổng quãng đường
        self.sub_plan = self.create_subscription(
            Path,
            '/plan',
            self.plan_callback,
            10)
            
        self.get_logger().info("-" * 60)
        self.get_logger().info("Node ĐO ĐẠC THÔNG SỐ NAV2 đã khởi động!")
        self.get_logger().info("HƯỚNG DẪN: Hãy đặt '2D Goal Pose' trên RViz2 để bắt đầu đo.")
        self.get_logger().info("-" * 60)

    def quaternion_to_yaw(self, q):
        """Chuyển đổi Quaternion sang góc Yaw (Radian)"""
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny_cosp, cosy_cosp)

    def plan_callback(self, msg):
        """Tính toán tổng chiều dài quãng đường dự kiến"""
        # Chỉ tính toán lại nếu có một plan mới (để tránh in liên tục)
        if len(msg.poses) < 2:
            return
            
        total_distance = 0.0
        # Cộng dồn khoảng cách giữa các điểm liên tiếp trong tuyến đường
        for i in range(len(msg.poses) - 1):
            x1 = msg.poses[i].pose.position.x
            y1 = msg.poses[i].pose.position.y
            x2 = msg.poses[i+1].pose.position.x
            y2 = msg.poses[i+1].pose.position.y
            
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            total_distance += dist
            
        # Nếu chiều dài mới chênh lệch đáng kể so với cũ (tránh nhiễu do replan liên tục)
        if abs(self.estimated_distance - total_distance) > 0.1:
            self.estimated_distance = total_distance
            print(f"\n[QUỸ ĐẠO MỚI] 🛣️ Khoảng cách di chuyển ước tính: {self.estimated_distance:.2f} mét")

    def goal_callback(self, msg):
        """Lưu lại tọa độ đích mong muốn"""
        self.goal_x = msg.pose.position.x
        self.goal_y = msg.pose.position.y
        self.goal_yaw = self.quaternion_to_yaw(msg.pose.orientation)
        
        print("\n" + "="*60)
        self.get_logger().info(f"📌 ĐÃ NHẬN MỤC TIÊU MỚI:")
        print(f"   -> Tọa độ Đích: X = {self.goal_x:.3f} m, Y = {self.goal_y:.3f} m")
        print(f"   -> Hướng Đích:  Yaw = {math.degrees(self.goal_yaw):.2f}°")
        print("="*60)

    def pose_callback(self, msg):
        """Tính toán và hiển thị sai số theo thời gian thực"""
        if self.goal_x is None:
            return
            
        current_x = msg.pose.pose.position.x
        current_y = msg.pose.pose.position.y
        current_yaw = self.quaternion_to_yaw(msg.pose.pose.orientation)

        # Tính sai số khoảng cách (cm)
        error_dist_cm = math.sqrt((current_x - self.goal_x)**2 + (current_y - self.goal_y)**2) * 100.0

        # Tính sai số góc (Độ)
        error_yaw_deg = math.degrees(current_yaw - self.goal_yaw)
        error_yaw_deg = (error_yaw_deg + 180) % 360 - 180
        error_yaw_deg = abs(error_yaw_deg)

        # In đè lên cùng 1 dòng
        sys.stdout.write(
            f"\r[ĐANG CHẠY] Sai số vị trí: {error_dist_cm:.2f} cm | Sai số góc: {error_yaw_deg:.2f}° "
        )
        sys.stdout.flush()

def main(args=None):
    rclpy.init(args=args)
    node = GoalErrorCalculator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nĐã dừng Node đo đạc.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()