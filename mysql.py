import mysql.connector
from mysql.connector import Error

class MySQLHelper:
    def __init__(self, host, user, password, database, port=3306):
        """初始化数据库连接"""
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            self.cursor = self.conn.cursor(dictionary=True)  # 查询结果返回字典形式
            print("MySQL 连接成功！")
        except Error as e:
            print(f"MySQL 连接失败: {e}")

    def query(self, sql, params=None):
        """执行查询操作"""
        try:
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"查询失败: {e}")
            return None

    def execute(self, sql, params=None):
        """执行插入、更新、删除操作"""
        try:
            self.cursor.execute(sql, params)
            self.conn.commit()
            return self.cursor.rowcount  # 返回受影响的行数
        except Error as e:
            self.conn.rollback()
            print(f"执行失败: {e}")
            return 0

    def insert(self, table, data):
        """插入数据"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
            return self.cursor.lastrowid  # 返回插入的最后一条记录的ID
        except Error as e:
            self.conn.rollback()
            print(f"插入失败: {e}")
            return None

    def update(self, table, data, condition):
        """更新数据"""
        try:
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            condition_clause = ' AND '.join([f"{key} = %s" for key in condition.keys()])
            sql = f"UPDATE {table} SET {set_clause} WHERE {condition_clause}"
            params = tuple(data.values()) + tuple(condition.values())
            self.cursor.execute(sql, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Error as e:
            self.conn.rollback()
            print(f"更新失败: {e}")
            return 0

    def delete(self, table, condition):
        """删除数据"""
        try:
            condition_clause = ' AND '.join([f"{key} = %s" for key in condition.keys()])
            sql = f"DELETE FROM {table} WHERE {condition_clause}"
            self.cursor.execute(sql, tuple(condition.values()))
            self.conn.commit()
            return self.cursor.rowcount
        except Error as e:
            self.conn.rollback()
            print(f"删除失败: {e}")
            return 0

    def close(self):
        """关闭数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("数据库连接已关闭")
        except Error as e:
            print(f"关闭连接失败: {e}")


if __name__ == "__main__":
    # 初始化工具类
    db = MySQLHelper(
        host="localhost",
        user="root",
        password="password",
        database="test_db"
    )

    # 查询操作
    result = db.query("SELECT * FROM your_table WHERE id = %s", (1,))
    print("查询结果:", result)

    # 插入操作
    new_id = db.insert("your_table", {"name": "John", "age": 30, "created_at": "2025-01-01"})
    print("插入的记录ID:", new_id)

    # 更新操作
    updated_rows = db.update("your_table", {"age": 35}, {"id": new_id})
    print("更新的行数:", updated_rows)

    # 删除操作
    deleted_rows = db.delete("your_table", {"id": new_id})
    print("删除的行数:", deleted_rows)

    # 关闭连接
    db.close()