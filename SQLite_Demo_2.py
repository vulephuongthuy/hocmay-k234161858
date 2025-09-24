import sqlite3
import pandas as pd

def top_customers_by_total_purchase(N=0):
    try:
        # Connect to DB and create a cursor
        sqliteConnection = sqlite3.connect('../database/Chinook_Sqlite.sqlite')
        cursor = sqliteConnection.cursor()
        print('DB Init')

        # Lấy dữ liệu Customer
        cursor.execute('SELECT * FROM Customer;')
        customer_columns = [desc[0] for desc in cursor.description]
        df_customers = pd.DataFrame(cursor.fetchall(), columns=customer_columns)

        # Lấy dữ liệu Invoice
        cursor.execute('SELECT * FROM Invoice;')
        invoice_columns = [desc[0] for desc in cursor.description]
        df_invoices = pd.DataFrame(cursor.fetchall(), columns=invoice_columns)

        # Chuyển cột Total sang số
        df_invoices['Total'] = df_invoices['Total'].astype(float)

        # Tính tổng giá trị mua hàng và số hóa đơn mỗi khách hàng
        customer_summary = df_invoices.groupby('CustomerId').agg(
            TotalPurchase=('Total', 'sum'),
            InvoiceCount=('InvoiceId', 'count')
        ).reset_index()

        # Lọc khách hàng có số hóa đơn >= N
        customer_summary = customer_summary[customer_summary['InvoiceCount'] >= N]

        # Kết hợp thông tin khách hàng
        result = df_customers.merge(customer_summary, on='CustomerId')

        # Sắp xếp giảm dần theo TotalPurchase và lấy top 10
        result = result.sort_values(by='TotalPurchase', ascending=False)

        # Close cursor
        cursor.close()

        return result

    except sqlite3.Error as error:
        print('Error occurred - ', error)
        return pd.DataFrame()

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')


# ---------------- Example ----------------
N = int(input("Nhập số hóa đơn tối thiểu N = "))
top_customers = top_customers_by_total_purchase(N)
print(top_customers)
