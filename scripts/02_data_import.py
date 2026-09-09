import pandas as pd
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='041019',
    database='taobao_analysis',
    charset='utf8mb4'
)

print("✅ 数据库连接成功！")


df = pd.read_csv(
    '../output/user_behavior_cleaned.csv'
)

print(f"✅ 读取数据成功，共 {len(df):,} 行")

print("\n数据字段：")
print(df.columns.tolist())

print("\n前5行数据：")
print(df.head())

cursor = conn.cursor()

cursor.execute(
    "TRUNCATE TABLE user_behavior;"
)

print("\n✅ 已清空 user_behavior 旧数据")

insert_sql = """
INSERT INTO user_behavior
(
    user_id,
    item_id,
    category_id,
    behavior_type,
    timestamp,
    date,
    date_only
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

data_to_insert = df[
    [
        'user_id',
        'item_id',
        'category_id',
        'behavior_type',
        'timestamp',
        'date',
        'date_only'
    ]
].values.tolist()
batch_size = 1000

for i in range(
    0,
    len(data_to_insert),
    batch_size
):

    batch = data_to_insert[
        i:i + batch_size
    ]

    cursor.executemany(
        insert_sql,
        batch
    )

    print(
        f"已处理：{min(i + batch_size, len(data_to_insert)):,} "
        f"/ {len(data_to_insert):,}"
    )
conn.commit()

print(
    f"\n✅ 成功导入 {len(df):,} 行数据到 MySQL"
)
cursor.close()

conn.close()

print("✅ MySQL连接已关闭")