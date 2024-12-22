from ssis.models.admin import Admin

def admin_found(username: str, password: str) -> bool:
    if Admin(username,password).registered_user():
        return True
    return False

import mysql.connector as mysql
from werkzeug.security import generate_password_hash

def is_invitation_code_valid(invitation_code: str) -> bool:
    # 在你的数据库中查询邀请码是否有效
    connection = mysql.connect(host='localhost', user='root', password='12345678', database='ssisdb')  # 请替换为你的数据库连接信息
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM invitations WHERE code = %s"
    cursor.execute(query, (invitation_code,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0] > 0  # 如果找到邀请码，则返回 True

import mysql.connector as mysql
from werkzeug.security import generate_password_hash

def register_user(username: str, password: str) -> int:
    try:
        # 使用 hashed 密码将用户添加到数据库
        hashed_password = generate_password_hash(password, method='sha256')
        connection = mysql.connect(host='localhost', user='root', password='12345678', database='ssisdb')
        cursor = connection.cursor()

        query = "INSERT INTO admin (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        connection.commit()  # 提交更改

        cursor.close()
        connection.close()
        
        return 1  # 注册成功，返回 1
    except Exception as e:
        print(f"Error: {e}")  # 打印错误信息
        return 0  # 注册失败，返回 0


