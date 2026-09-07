import pandas as pd
import pymysql

# 1. 建立数据库连接
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='041019',  
    database='taobao_analysis',
    charset='utf8mb4'    
)

print("✅ 数据库连接成功！")

# 2. 读取清洗后的数据
df = pd.read_csv('../output/user_behavior_cleaned.csv')
print(f"✅ 读取数据成功，共 {len(df)} 行")

# 3. 逐行插入数据（或使用批量插入）
cursor = conn.cursor()

# 清空旧数据（如果有）
cursor.execute("TRUNCATE TABLE user_behavior;")

# 批量插入（每1000条提交一次）
insert_sql = """
INSERT INTO user_behavior (user_id, item_id, category_id, behavior_type, timestamp, date, date_only)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
data_to_insert = [tuple(row) for row in df.to_numpy()]

# 分批插入，避免一次性内存爆炸
batch_size = 1000
for i in range(0, len(data_to_insert), batch_size):
    cursor.executemany(insert_sql, data_to_insert[i:i+batch_size])
    print(f"已插入 {i+len(data_to_insert[i:i+batch_size])} 行...")

conn.commit()
print(f"✅ 成功导入 {len(df)} 行数据到 MySQL.taobao_analysis.user_behavior")

cursor.close()
conn.close()