import psycopg2

# 配置 PostgreSQL 数据库
def get_db_connection():
    conn = psycopg2.connect(
        dbname="9900tempDB",
        user="postgres",
        password="123456",
        host="localhost",
        port=5432
    )
    return conn

# 执行 SQL 查询
def query_db(query, params=()):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    conn.commit()  # 提交事务
    conn.close()
    return results
