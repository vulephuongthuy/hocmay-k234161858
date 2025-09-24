import pandas as pd

def find_orders_within_range(df, minValue, maxValue, SortType=True):
    # tổng giá trị từng đơn hàng
    order_totals = df.groupby('OrderID').apply(lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum())
    # lọc đơn hàng trong range
    orders_within_range = order_totals[(order_totals >= minValue) & (order_totals <= maxValue)]
    # Sắp xếp theo soft type
    orders_within_range = orders_within_range.sort_values(ascending=SortType)
    # danh sách các mã đơn hàng không trùng nhau
    result = [{'OrderID': idx, 'TotalValue': val} for idx, val in orders_within_range.items()]

    return result

df = pd.read_csv('../dataset/SalesTransactions.csv')

minValue = float(input("Nhập giá trị min: "))
maxValue = float(input("Nhập giá trị max: "))
SortType = input("Sắp xếp tăng dần? (y/n): ").strip().lower() == 'y'
result = find_orders_within_range(df, minValue, maxValue, SortType)
print('Danh sách các hóa đơn trong phạm vi giá trị từ', minValue, 'đến', maxValue, ' là:', result)
for r in result:
    print(r)
