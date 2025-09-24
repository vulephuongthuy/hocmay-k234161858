import pandas as pd

def top_3_products_by_sales(df):
    # Tính giá trị bán ra của từng dòng
    df['TotalSales'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

    # Nhóm theo ProductID và tính tổng giá trị bán ra
    product_totals = df.groupby('ProductID')['TotalSales'].sum().reset_index()

    # Sắp xếp giảm dần theo tổng giá trị và lấy top 3
    top_products = product_totals.sort_values(by='TotalSales', ascending=False).head(3)
-
    return top_products

# ---------------- Example ----------------
df = pd.read_csv('../dataset/SalesTransactions.csv')

top3 = top_3_products_by_sales(df)
print("3 sản phẩm có tổng giá trị bán ra cao nhất:")
print(top3)
