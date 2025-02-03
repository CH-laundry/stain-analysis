from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "污漬分析系統運行中"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
