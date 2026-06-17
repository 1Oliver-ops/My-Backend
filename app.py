from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许前端的请求

# 模拟数据库（用字典存用户）
users_db = {}

# ===== 注册接口 =====
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "邮箱和密码不能为空"}), 400

    if email in users_db:
        return jsonify({"success": False, "message": "该邮箱已被注册"}), 400

    # 保存用户（实际项目中密码需要加密）
    users_db[email] = {"password": password}
    return jsonify({"success": True, "message": "注册成功！", "user": email})

# ===== 登录接口 =====
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

# ===== 验证用户接口 =====
@app.route("/api/me", methods=["GET"])
def get_user():
    token = request.headers.get("Authorization")
    
    if not token:
        return jsonify({"success": False, "message": "未登录"}), 401

    # 简单模拟：从 token 里提取邮箱（实际项目用 JWT 解析）
    if token == "Bearer fake-jwt-token-12345":
        return jsonify({"success": True, "user": "test@example.com"})
    
    return jsonify({"success": False, "message": "token 无效"}), 401

if __name__ == "__main__":
    app.run(port=5000, debug=True)