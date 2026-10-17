from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    # 首页路由：返回问候语
    return "Hello, NEU!"


if __name__ == "__main__":
    # 监听所有网卡，便于头歌端口映射后外部访问
    app.run(host="0.0.0.0", port=5000)
