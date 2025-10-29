from flask import Flask, render_template_string
from flaskext.mysql import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np
app = Flask(__name__)

def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
        #MySQL configurations
        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = database
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except mysql.connector.Error as e:
        print("Error = ", e)
    return None
def closeConnection(conn):
    if conn!= None:
        conn.close()
def queryDataset(conn,sql):
    cursor = conn.cursor()

    cursor.execute(sql)
    df=pd.DataFrame(cursor.fetchall())
    return df
conn = getConnect('localhost', 3306, 'salesdatabase', 'root', '@Obama123')

sql1="select * from customer"
df1=queryDataset(conn,sql1)
print(df1)

sql2 = (
    "SELECT DISTINCT customer.CustomerId, Age, Annual_Income, Spending_Score "
    "FROM customer, customer_spend_score "
    "WHERE customer.CustomerId = customer_spend_score.CustomerID"
)

df2=queryDataset(conn, sql2)
df2.columns = ['CustomerId', 'Age', 'Annual Income', 'Spending Score']

print(df2)

print(df2.head())

print(df2.describe())

def showHistogram(df, columns):
    plt.figure(1, figsize = (7,8))
    n = 0
    for column in columns:
        n += 1
        plt.subplot(3,1,n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.distplot(df[column], bins=32, kde=True, color='skyblue')
        plt.title(f'Histogram of {column}')
    plt.show()

showHistogram(df2, df2.columns[1:])

def elbowMethod(df, columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters = n,
                       init = 'k-means++',
                       max_iter=500,
                       random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(1, figsize = (15,6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '-', alpha = 0.5)
    plt.xlabel('Number of Clusters'), plt.ylabel('Cluster sum of squared distances')
    plt.show()
columns=['Age', 'Spending Score']
elbowMethod(df2, columns)

def runKMeans(X, cluster):
    model = KMeans(n_clusters=cluster,
                   init='k-means++',
                   max_iter=500,
                   random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans =  model.fit_predict(X)
    return y_kmeans,centroids,labels

X =  df2.loc[:, columns].values
cluster=4
colors=['red', 'green', 'blue', 'purple', 'black', 'pink', 'orange']

y_kmeans, centroids, labels=runKMeans(X, cluster)
print(y_kmeans)
print(centroids)
print(labels)
df2["cluster"]=labels

def visualizeKMeans(X,y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize=(10,10))
    for i in range(cluster):
        plt.scatter(X[y_kmeans == i, 0],
                    X[y_kmeans == i, 1],
                    s=100,
                    c=colors[i],
                    label='Cluster %i'%(i+1))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend
    plt.show()
visualizeKMeans(X, y_kmeans,
                cluster,
                "Clusters of Customers - Age X Spending Score",
                "Age",
                "Spending Score",
                colors)

columns=['Annual Income', 'Spending Score']
elbowMethod(df2,columns)

X = df2.loc[:, columns].values
cluster=5

y_kmeans, centroids, labels=runKMeans(X, cluster)

print(y_kmeans)
print(centroids)
print(labels)
df2["cluster"]=labels

visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Cluster of Customer - Annual Income X Spending Score",
                "Annual Income",
                "Spending Score", colors)

columns=['Age', 'Annual Income', 'Spending Score']
elbowMethod(df2, columns)

X = df2.loc[:, columns].values
cluster=6

y_kmeans, centroids, labels=runKMeans(X, cluster)

print(y_kmeans)
print(centroids)
print(labels)
df2["cluster"]=labels
print(df2)

def visualize3DKMeans(df, columns, hover_data, cluster):
    fig = px.scatter_3d(df,
                        x=columns[0],
                        y=columns[1],
                        z=columns[2],
                        color='cluster',
                        hover_data=hover_data,
                        category_orders={"cluster":range(0,cluster)},
                        )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()
hover_data=df2.columns
visualize3DKMeans(df2, columns, hover_data, cluster)


def showClusterDetails(df, cluster_column='cluster'):
    """
    Hiển thị danh sách chi tiết các khách hàng theo từng cluster
    :param df: DataFrame chứa dữ liệu khách hàng, có cột cluster
    :param cluster_column: tên cột lưu nhãn cluster
    """
    clusters = df[cluster_column].unique()
    clusters.sort()  # sắp xếp theo cluster

    for c in clusters:
        print(f"\n===== Cluster {c} =====")
        cluster_df = df[df[cluster_column] == c]
        print(cluster_df.to_string(index=False))  # in toàn bộ chi tiết, không in index
        print(f"Total customers in Cluster {c}: {len(cluster_df)}")
showClusterDetails(df2)

@app.route("/clusters")
def show_cluster_web():
    """
    Hiển thị chi tiết các khách hàng theo từng cluster trên web
    """
    clusters = df2['cluster'].unique()
    clusters.sort()

    # Tạo nội dung HTML
    html_content = "<h1>Customer Clusters Details</h1>"
    for c in clusters:
        html_content += f"<h2>Cluster {c}</h2>"
        cluster_df = df2[df2['cluster'] == c]
        # Chuyển DataFrame thành HTML table
        html_content += cluster_df.to_html(index=False, classes='table table-striped', border=1)
        html_content += f"<p><strong>Total customers in Cluster {c}: {len(cluster_df)}</strong></p>"

    return render_template_string(html_content)
if __name__ == "__main__":
    app.run(debug=True)