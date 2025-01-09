#-*- coding : utf-8-*-
# coding:utf-8

import pymysql


class MysqlTool:
    def __init__(self):
        """mysql 连接初始化"""
        self.host = '219.151.150.135'
        self.port = 3306
        self.user = 'zgdb'
        self.password = 'zgdb@888'
        self.db = 'robot_manage'
        self.charset = 'utf8'
        self.mysql_conn = None

    def __enter__(self):
        """打开数据库连接"""
        self.mysql_conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.password,
            db=self.db,
            charset=self.charset
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """关闭数据库连接"""
        if self.mysql_conn:
            self.mysql_conn.close()
            self.mysql_conn = None

    def execute(self, sql: str, args: tuple = None, commit: bool = False) -> any:
        """执行 SQL 语句"""
        try:
            with self.mysql_conn.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    self.mysql_conn.commit()
                    print(f"执行 SQL 语句：{sql}，参数：{args}，数据提交成功")
                else:
                    result = cursor.fetchall()
                    print(f"执行 SQL 语句：{sql}，参数：{args}，查询到的数据为：{result}")
                    return result
        except Exception as e:
            print(f"执行 SQL 语句出错：{e}")
            self.mysql_conn.rollback()
            raise e


#引入mysql工具类
#from mysql_tool import MysqlTool

if __name__ == '__main__':
    with MysqlTool() as db:
        # 查询所有数据
        sql = 'SELECT * FROM student'
        result = db.execute(sql)
        print(f"查询到的数据为：{result}")

        # 带条件的查询
        sql = "SELECT * FROM student WHERE age > %s"
        args = (18,)
        result = db.execute(sql, args)
        print(f"年龄大于18岁的学生：{result}")

        # 单条插入
        sql = "INSERT INTO student(name, age) VALUES (%s, %s)"
        args = ('张三', 22)
        db.execute(sql, args, commit=True)

        # 多条插入
        sql = "INSERT INTO student(name, age) VALUES (%s, %s)"
        args_list = [('李四', 20), ('王五', 21), ('赵六', 23)]
        for args in args_list:
            db.execute(sql, args, commit=True)

        # 修改数据
        sql = "UPDATE student SET age=%s WHERE name=%s"
        args = (23, '张三')
        db.execute(sql, args, commit=True)

        # 删除数据
        sql = "DELETE FROM student WHERE name=%s"
        args = ('张三',)
        db.execute(sql, args, commit=True)
