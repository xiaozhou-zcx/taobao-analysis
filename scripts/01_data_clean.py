import pandas as pd

# 读取数据,只读取前20w行,因为数据太多了
df = pd.read_csv('../data/UserBehavior.csv', header=None, nrows=600000)

# 添加列名
df.columns = ['user_id', 'item_id', 'category_id', 'behavior_type', 'timestamp']

# 查看数据概况
print(f'原始数据量: {len(df)} 行')
print(f'列名: {df.columns.tolist()}')
print(df.head())

# 检查空值
print(f'\n空值统计:\n{df.isnull().sum()}')

# 删除重复行
df = df.drop_duplicates()
print(f'去重后数据量: {len(df)} 行')

# 转换时间戳
df['date'] = pd.to_datetime(df['timestamp'], unit='s')
print('时间戳转换成成功（秒级）')
# 提取日期（用于后续分析）
df['date_only'] = df['date'].dt.date

# 保存清洗后的数据
df.to_csv('../output/user_behavior_cleaned.csv', index=False)
print(f'\n✅ 清洗完成！最终数据量: {len(df)} 行')
print(f'清洗后文件保存在: output/user_behavior_cleaned.csv')