# coding:utf8
from app import app

if __name__ == "__main__":
    # app.run()的默认参数为“host="127.0.0.1"”，此时外部不能访问，
    # 当参数为“host="0.0.0.0"”时可以通过外部访问。
    app.run(host="0.0.0.0")
