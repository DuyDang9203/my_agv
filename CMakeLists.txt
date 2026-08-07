cmake_minimum_required(VERSION 3.8)
project(my_agv)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()

  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_dummy test/test_dummy.cpp)
endif()

# =========================================================================
# ĐÃ SỬA: Thêm 'config' và 'maps' vào danh sách cài đặt
# =========================================================================
install(DIRECTORY
  urdf
  launch
  rviz
  worlds
  config   
  maps     
  DESTINATION share/${PROJECT_NAME}
)

ament_package()