import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Rajvardhan@1212',
        database='social_engagement_db',
        port=3306
    )
    
    if connection.open:
        print("Success: Connected to social_engagement_db!")
        connection.close()

except Exception as e:
    print(f"Error connecting to database: {e}")
