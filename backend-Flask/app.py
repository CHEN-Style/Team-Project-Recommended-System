from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_connection

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 检查连接
@app.route('/')
def home():
    return "hello world"

# 获取所有用户
@app.route('/admin/user', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({
        "code": 200,
        "data": users,
        "message": "user form query success"
    })

# 用户注册
@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")  # 实际应用中应该加密存储

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING name, email",
        (name, email, password)
    )
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "code": 200,
        "data": {"name": user[0], "email": user[1]},
        "message": "insert success"
    })

# 用户登录
@app.route('/user/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, password_hash FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "user email invalid"}), 400

    if user[3] != password:
        return jsonify({"error": "密码错误"}), 400

    return jsonify({
        "message": "登录成功",
        "user": {"id": user[0], "name": user[1], "email": user[2]}
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)

