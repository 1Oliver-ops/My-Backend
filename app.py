from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 模拟数据库（用字典存用户）
users_db = {}

@app.route("/")
def home():
    return "Python 后端运行正常！"

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "邮箱和密码不能为空"}), 400

    if email in users_db:
        return jsonify({"success": False, "message": "该邮箱已被注册"}), 400

    users_db[email] = {"password": password}
    return jsonify({"success": True, "message": "注册成功！", "user": email})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "邮箱和密码不能为空"}), 400

    user = users_db.get(email)
    if not user or user["password"] != password:
        return jsonify({"success": False, "message": "邮箱或密码错误"}), 401

    return jsonify({
        "success": True,
        "message": "登录成功！",
        "user": email,
        "token": "fake-jwt-token-12345"
    })

@app.route("/api/me", methods=["GET"])
def get_user():
    token = request.headers.get("Authorization")
    
    if not token:
        return jsonify({"success": False, "message": "未登录"}), 401

    if token == "Bearer fake-jwt-token-12345":
        return jsonify({"success": True, "user": "test@example.com"})
    
    return jsonify({"success": False, "message": "token 无效"}), 401

# ===== Vercel 需要这个 =====
vercel_app = app

# ===== 本地运行用 =====
if __name__ == "__main__":
    app.run(port=5000, debug=True)