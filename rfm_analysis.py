import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# RFM用户价值分析
df = pd.read_excel("Amazon_Sales_Data.xlsx")
df["Order Date"] = pd.to_datetime(df["Order Date"])
analysis_date = pd.to_datetime("2024-07-31")

# 计算RFM
rfm = df.groupby("Customer ID").agg({
    "Order Date": lambda x: (analysis_date - x.max()).days,
    "Order ID": "count",
    "Sales": "sum"
}).reset_index()
rfm.columns = ["Customer ID", "R", "F", "M"]

# 打分
rfm["R_score"] = pd.qcut(rfm["R"], 5, labels=[5,4,3,2,1], duplicates='drop')
rfm["F_score"] = pd.qcut(rfm["F"], 5, labels=[1,2,3,4,5], duplicates='drop')
rfm["M_score"] = pd.qcut(rfm["M"], 5, labels=[1,2,3,4,5], duplicates='drop')
rfm["RFM_score"] = rfm["R_score"].astype(int) + rfm["F_score"].astype(int) + rfm["M_score"].astype(int)

# 分层
def segment(row):
    r, f, m = int(row["R_score"]), int(row["F_score"]), int(row["M_score"])
    if r >= 4 and f >= 4 and m >= 4: return "VIP客户"
    elif f >= 4 and m >= 4: return "潜力客户"
    elif r >= 4: return "价值客户"
    elif r <= 2: return "流失预警"
    else: return "普通客户"

rfm["用户类型"] = rfm.apply(segment, axis=1)

# 输出结果
print(rfm["用户类型"].value_counts())
print(rfm.groupby("用户类型")["M"].mean())
