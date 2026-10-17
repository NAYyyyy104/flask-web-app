import sys
import unittest
from pathlib import Path

# 将项目根目录加入模块搜索路径，使 tests 可以导入 src 包
sys.path.append(str(Path(__file__).parent.parent))

from src.app import app  # noqa: E402


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        # 创建测试客户端
        app.testing = True
        self.app = app.test_client()

    def test_hello_world(self):
        # 测试首页
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Hello, World!")


if __name__ == "__main__":
    unittest.main()
