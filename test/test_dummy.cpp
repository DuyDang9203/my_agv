#include <gtest/gtest.h>

TEST(DummyTest, BasicAssertions) {
  // Test if true is indeed true
  EXPECT_TRUE(true);
  
  // Test simple arithmetic
  EXPECT_EQ(1 + 1, 2);
}

int main(int argc, char **argv) {
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
