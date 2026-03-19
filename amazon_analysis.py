import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_excel("Amazon_Sales_Data.xlsx")

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

print("=" * 60)
print("              Amazon Sales Data Analysis")
print("=" * 60)

# 1. 数据概况
print(f"\n总订单数：{len(df)}")
print(f"总销售额：${df['Sales'].sum():,.2f}")
print(f"平均客单价：${df['Sales'].mean():,.2f}")
print(f"客户数量：{df['Customer ID'].nunique()}")

# 2. 月度销售
monthly = df.groupby("Month")["Sales"].sum()
print(f"\n月度销售最高：{monthly.idxmax()}月 (${monthly.max():,.2f})")

# 3. 品类销售
category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
print(f"\n品类销售冠军：{category.index[0]} (${category.iloc[0]:,.2f})")

# 4. 城市销售
city = df.groupby("City")["Sales"].sum().sort_values(ascending=False)
print(f"\n城市销售冠军：{city.index[0]} (${city.iloc[0]:,.2f})")

# 5. 客户分层
customer = df.groupby("Customer ID")["Sales"].sum()
high_value = customer[customer > 2000].count()
print(f"\n高价值客户（>2000$）：{high_value}人")

# 6. 评价分析
rating5 = (df["Rating"] == 5).sum() / len(df) * 100
print(f"\n五星好评率：{rating5:.1f}%")

print("\n" + "=" * 60)
print("                   分析完成！")
print("=" * 60)

# 保存图表
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

monthly_m = monthly / 1e6
axes[0,0].bar(monthly_m.index, monthly_m.values, color='steelblue')
axes[0,0].set_title("Monthly Sales Trend")

category_m = category / 1e6
axes[0,1].barh(category_m.index, category_m.values, color='coral')
axes[0,1].set_title("Sales by Category")

city_m = city / 1e6
axes[1,0].barh(city_m.index, city_m.values, color='seagreen')
axes[1,0].set_title("Sales by City")

rating = df["Rating"].value_counts().sort_index()
axes[1,1].pie(rating.values, labels=rating.index, autopct='%1.1f%%')
axes[1,1].set_title("Rating Distribution")

plt.tight_layout()
plt.savefig("sales_analysis.png", dpi=150)
plt.show()
